from __future__ import annotations

import unittest

import cohdl
from cohdl import vhdl as RawVhdl
from cohdl.utility import IndentBlock, MakeTarget

from pathlib import Path
import subprocess
import tempfile
import shutil

from .formal._builtins import _set_formal_tools_active


class vhdl(RawVhdl):
    def post_process(self, text: str):
        text = text.replace("<%", "{")
        return text.replace("%>", "}")


class YosysProject:
    def __init__(self):
        self._tasks = []
        self._options = []
        self._engines = []
        self._script = []
        self._files = []

    def add_task(self, task: str):
        self._tasks.append(task)

    def add_option(self, option: str):
        self._options.append(option)

    def add_engine(self, engine: str):
        self._engines.append(engine)

    def add_script(self, script: str):
        self._script.append(script)

    def add_file(self, files: str):
        self._files.append(files)

    def write(self, file_path):
        with open(file_path, "w") as file:

            def write_section(sec_name, content):
                print(f"[{sec_name}]", file=file)

                for line in content:
                    print(line, file=file)

                print(file=file)

            write_section("tasks", self._tasks)
            write_section("options", self._options)
            write_section("engines", self._engines)
            write_section("script", self._script)
            write_section("files", self._files)


class YosysParams:
    @staticmethod
    def _make_default():
        return YosysParams(
            build_dir="build",
            clean_build_dir=False,
            bmc=False,
            cover=False,
            prove=False,
            live=False,
            engines=["smtbmc"],
            multiclock=False,
            files=set(),
            reserved_names=set(),
            use_absolute_paths=False,
            use_tmp_dir=False,
            unittest_name="test_formal_properties",
            instance_name="dut",
            quiet=False,
        )

    def __init__(
        self,
        *,
        build_dir: str = None,
        clean_build_dir=None,
        bmc=None,
        bmc_depth: int = None,
        cover: bool = None,
        cover_depth: int = None,
        prove: bool = None,
        prove_depth: int = None,
        live: bool = None,
        engines: str | list[str] = None,
        max_jobs: int = None,
        multiclock: bool = None,
        files: set[str] = None,
        reserved_names: set[str] = None,
        use_absolute_paths: bool = None,
        use_tmp_dir: bool = None,
        unittest_name: str = None,
        no_rebuild: bool = None,
        instance_name: str = None,
        quiet: bool = None,
        architecture_name: str | None = None,
    ):
        self._build_dir = build_dir
        self._clean_build_dir = clean_build_dir

        # bounded model check
        # prove that all assertions hold for checked depth
        self._bmc = bmc
        self._bmc_depth = bmc_depth

        # check that is is possible to cover all
        # cover statements in the given duration
        self._cover = cover
        self._cover_depth = cover_depth

        # prove that assertions hold at ALL times
        # by running a bmc with the given depth
        # and performing and induction step to extend
        # the result to all future time points
        self._prove = prove
        self._prove_depth = prove_depth

        # checks that cover statements with infinite wait durations
        # can eventually be covered
        # (by proving that there are no loops/deadlocks that could
        # prevent this)
        self._live = live

        self._engines = [engines] if isinstance(engines, str) else engines
        self._max_jobs = max_jobs
        self._multiclock = multiclock
        self._files = files
        self._reserved_names = reserved_names
        self._use_absolute_paths = use_absolute_paths
        self._use_tmp_dir = use_tmp_dir
        self._unittest_name = unittest_name

        self._no_rebuild = no_rebuild
        self._instance_name = instance_name
        self._quiet = quiet
        self._architecture_name = architecture_name


def _collect_class_params(
    cls: type, initial_result, member_name: str, handlers: dict[str] = {}
):
    result = initial_result

    for elem in cls.mro()[::-1]:
        member_elem: YosysParams = elem.__dict__.get(member_name, None)

        if member_elem is None:
            continue

        assert isinstance(
            member_elem, type(initial_result)
        ), f"member '{member_name}' of '{cls}' should be an instance of '{type(initial_result)}' not {member_elem}"

        for name, val in member_elem.__dict__.items():
            assert name in result.__dict__

            if val is None:
                continue

            if name not in handlers:
                result.__dict__[name] = val
            else:
                result.__dict__[name] = handlers[name](result.__dict__[name], val)

    return result


class YosysTestCase(unittest.TestCase):

    def __init_subclass__(cls, **kwargs):

        if "entity" in kwargs:
            assert not hasattr(
                cls, "_yosys_entity"
            ), "entity has already been specified in base class"

            cls._yosys_entity = kwargs["entity"]
            del kwargs["entity"]

            assert hasattr(cls, "_yosys_params_"), "missing class member _yosys_params_"
            assert hasattr(cls, "architecture"), "missing class member architecture"

            params: YosysParams = _collect_class_params(
                cls,
                YosysParams._make_default(),
                "_yosys_params_",
                handlers={
                    "files": set.union,
                    "reserved_names": set.union,
                },
            )

            def test_formal_properties(self: YosysTestCase, return_on_error=False):

                yosys = Yosys(tested_entity=cls._yosys_entity, params=params)

                def architecture(entity):
                    self.architecture(entity)

                yosys.architecture(architecture)

                def build_and_run(build_dir):
                    if not params._no_rebuild:
                        yosys.build(build_dir=build_dir)
                    ret = yosys.run(build_dir=build_dir)

                    if ret == 0:
                        return True

                    if return_on_error:
                        return False

                    assert (
                        ret == 0
                    ), f"formal verification failed with exit code '{ret}'"

                if params._use_tmp_dir:
                    assert (
                        not params._no_rebuild
                    ), "no_rebuild parameter should not be used in combination with temporary build directory"
                    with tempfile.TemporaryDirectory() as tmpdir:
                        return build_and_run(tmpdir)
                else:

                    if params._clean_build_dir and Path(params._build_dir).exists():
                        shutil.rmtree(params._build_dir)

                    return build_and_run(params._build_dir)

            def __init__(self, methodName: str = params._unittest_name):
                super().__init__(methodName=methodName)

            setattr(cls, params._unittest_name, test_formal_properties)
            setattr(cls, "__init__", __init__)

        assert len(kwargs) == 0, f"received unexpected keyword arguments {kwargs}"

        return super().__init_subclass__()


class Yosys:
    class ProjPaths:
        def __init__(self, build_dir):
            self.dir_build = build_dir
            self.dir_generated = f"{build_dir}/"
            self.dir_generated_vhdl = f"{build_dir}/"
            self.dir_generated_formal = f"{build_dir}/"
            self.makefile = f"{build_dir}/Makefile"
            self.psl_file = f"{build_dir}/project.psl"
            self.sby_file = f"{build_dir}/project.sby"

        def create_dirs(self):
            for path in [
                self.dir_build,
                self.dir_generated,
                self.dir_generated_vhdl,
                self.dir_generated_formal,
            ]:
                Path(path).mkdir(parents=True, exist_ok=True)

        def relative(self, name: str):
            return self.relative_to_build(getattr(self, name))

        def relative_to_build(self, path: str, keep_absolute=False) -> str:
            if keep_absolute and Path(path).is_absolute():
                return path
            return str(Path(path).relative_to(self.dir_build, walk_up=True))

        def local_or_absolute(self, path: Path):
            path = Path(path)
            return str(path) if path.is_absolute() else str(path.name)

    def __init__(
        self,
        tested_entity: type[cohdl.Entity],
        *,
        params: YosysParams,
    ):
        self._entity = tested_entity
        self._arch = None

        self._params = params

    def assertions(self, fn):
        return cohdl.std.concurrent(fn)

    def architecture(self, fn):
        self._arch = fn

    def build(self, build_dir, *, run=False):
        try:
            _set_formal_tools_active(True)
            self._build_impl(build_dir, run=run)
        finally:
            _set_formal_tools_active(False)

    def _build_impl(self, build_dir, *, run=False):

        from .formal._checker import _used_labels

        # clear dict of used names before build
        _used_labels.clear()

        paths = self.ProjPaths(build_dir)
        paths.create_dirs()

        params = self._params

        #
        # write vhdl files
        #

        reserved_names = set(params._reserved_names)
        files = set() if params._files is None else set(params._files)

        if not self._entity._cohdl_info.extern:
            vhdl_lib = cohdl.std.VhdlCompiler.to_vhdl_library(self._entity)
            top_arch = vhdl_lib.top_entity().architecture()
            entity_name = top_arch.entity_name()
            arch_name = top_arch.arch_name()

            files.update(vhdl_lib.write_dir(paths.dir_generated_vhdl))

            # find all names already used in the entity
            # to avoid name collisions

            reserved_names.update(top_arch.scope().declarations().keys())
        else:

            entity_name = self._entity._cohdl_info.name

            if params._architecture_name is not None:
                arch_name = params._architecture_name
            else:
                attributes = self._entity._cohdl_info.attributes
                arch_name = attributes.get("arch_name", None)

        #
        # write psl file
        #

        ports = {}

        for name, value in self._entity._cohdl_info.ports.items():
            ports[name] = cohdl.Port.inout(value.type, name=name)

        formal_entity = type(
            "YosysEntity",
            (self._entity,),
            {**ports, "architecture": self._arch},
            attributes={"reserved_names": reserved_names},
        )

        vhdl_lib = cohdl.std.VhdlCompiler.to_vhdl_library(formal_entity)
        top_entity = vhdl_lib.top_entity()
        top_arch = top_entity.architecture()

        arch_str = "" if arch_name is None else f"({arch_name})"

        psl_content = IndentBlock(
            [
                f"vunit {params._instance_name}({entity_name}{arch_str})" "{",
                top_arch.write_declarations(),
                top_arch.write_instances(),
                "}",
            ]
        )

        with open(paths.psl_file, "w") as file:
            print(psl_content, file=file)

        files.add(paths.psl_file)

        #
        # write sby file
        #

        proj = YosysProject()

        if params._bmc:
            proj.add_task("bmc")
            proj.add_option("bmc: mode bmc")

            if params._bmc_depth is not None:
                proj.add_option(f"bmc: depth {params._bmc_depth}")

        if params._cover:
            proj.add_task("cover")
            proj.add_option("cover: mode cover")

            if params._cover_depth is not None:
                proj.add_option(f"cover: depth {params._cover_depth}")

        if params._prove:
            proj.add_task("prove")
            proj.add_option("prove: mode prove")

            if params._prove_depth is not None:
                proj.add_option(f"prove: depth {params._prove_depth}")

        if params._live:
            proj.add_task("live")
            proj.add_option("live: mode live")

        if params._multiclock:
            proj.add_option("multiclock on")

        for engine in params._engines:
            proj.add_engine(engine)

        if params._use_absolute_paths:
            files = [str(Path(file).absolute()) for file in files]
        else:
            # when relative paths are used, the file section is required
            # to move the files to the appropriate location
            relative_files = [
                paths.relative_to_build(file, keep_absolute=True) for file in files
            ]

            for file in relative_files:
                proj.add_file(file)

        # Yosys copies files at relative paths into a src directory and
        # changes into it before runing the script section.
        # Hence all relative paths must be preplaced with their file name.
        local_or_absolute_files = [paths.local_or_absolute(file) for file in files]

        proj.add_script(
            f"ghdl --std=08 {' '.join(local_or_absolute_files)} -e {entity_name}"
        )
        proj.add_script(f"prep -top {entity_name}")

        proj.write(paths.sby_file)

        #
        # write Makefile
        #

        if params._max_jobs is None:
            opt_max_jobs = ""
        elif isinstance(params._max_jobs, int):
            opt_max_jobs = f"-j {params._max_jobs}"
        else:
            assert (
                params._max_jobs == "auto"
            ), "parameter 'max_jobs' must be an integer or the string 'auto'"

            import multiprocessing

            opt_max_jobs = f"-j {multiprocessing.cpu_count()}"

        root_target = MakeTarget(
            "all",
            f'sby --yosys "yosys -m ghdl" -f {paths.relative_to_build(paths.sby_file)} {opt_max_jobs}',
        )

        root_target.generate_makefile(path=paths.makefile)

        if run:
            ret = self.run(build_dir=build_dir)

            if ret != 0:
                exit(ret)

    def run(self, build_dir):
        stdout = subprocess.DEVNULL if self._params._quiet else None

        return subprocess.call(["make", "-C", build_dir], stdout=stdout, stderr=stdout)
