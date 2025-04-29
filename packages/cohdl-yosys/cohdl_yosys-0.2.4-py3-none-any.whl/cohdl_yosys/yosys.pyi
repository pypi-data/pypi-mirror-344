from __future__ import annotations

import unittest
from typing import Literal

import cohdl

class YosysParams:
    def __init__(
        self,
        *,
        build_dir: str | None = None,
        clean_build_dir: bool | None = None,
        use_tmp_dir: bool | None = None,
        bmc: bool | None = None,
        bmc_depth: int | None = None,
        cover: bool | None = None,
        cover_depth: int | None = None,
        prove: bool | None = None,
        prove_depth: int | None = None,
        live: bool | None = None,
        engines: str | list[str] | None = None,
        max_jobs: int | Literal["auto"] | None = None,
        multiclock: bool | None = None,
        files: set[str] | None = None,
        reserved_names: set[str] | None = None,
        use_absolute_paths: bool | None = None,
        unittest_name: str | None = None,
        instance_name: str | None = None,
        quiet: bool | None = None,
        architecture_name: str | None = None,
    ):
        """
        Contains all configuration parameters for the Yosys invokation.

        * build_dir

            directory for generated files, defaults to "build"

        * clean_build_dir

            when set to True, the build directory is deleted
            and recreated before each test run

        * use_tmp_dir

            when set to True, `build_dir` is ignored and replaced
            with a remporary directory that is deleted once the test is done
            (only supported in a YosysTestCase)

        * bmc, bmc_depth

            When `bmc` is set to True, a bounded model check is performed.
            `bmc_depht` defines the number of steps during this check
            and defaults to 20.

        * cover, cover_depth

            When `cover` is set to True, a coverage check is performed.
            `cover_depth` defines the number of steps during this check
            and defaults to 20.

        * prove, prove_depth

            When `prove` is set to True, Yosys attempts to prove that
            assertions will always hold.
            `prove_depth` defines the k-induction depth and defaults to 20.

        * live

            When `live` is set to True, a liveliness check is performed.
            This affects cover statements with infinite durations that should
            eventually hold. The solver attempts to find a deadlock/infinte loop
            that will never reach the end state of the cover statement.

        * engines

            Every entry in this list is added to the [engines] section
            of the generated .sby file. Check the Yosys documentation for details.
            Defaults to ["smtbmc"].

        * max_jobs

            Limit for number of used threads.
            Sets the '-j' option of the sby command.
            Defaults to single-threaded.
            Use `max_jobs="auto"` to autodetect available thread count.

        * multiclock

            Perform a test with support for multiple clocks.

        * files

            When a test requires additional files, for example to
            refere to external VHDL entities, the paths must be
            added to this set so Yosys can find them.

        * reserved_names

            The Python->VHDL/PSL compilation can introduce name conflicts
            with identifiers used in the design under test or Yosys builtins.
            Such names can be added to this set to prevent the compiler
            from using them.

        * use_absolute_paths

            By default Yosys copies needed files to `build_dir`.
            When this option is set to True, paths are converted to
            their absolute location and used inplace.

        * unittest_name

            The Python unittest framework, underlying YosysTestCase,
            searches test methods based on their name.
            The default name used by YosysTestCase ('test_formal_properties')
            can be overwritten using the `unittest_name` parameter to allow
            for custom naming conventions.

        * instance_name

            Name of the tested instance, shows up in Yosys output.
            Defaults to 'dut'.

        * architecture_name

            Optional name of the tested VHDL architecture.
        """

class YosysTestCase(unittest.TestCase):
    """
    YosysTestCase derives from unittest.TestCase
    to allow automated test execution and integration
    into IDEs/vscode.

    ---

    Subclasses of YosysTestCase usually have two class members:

    * _yosys_params_

        An instance of YosysParams that configures the test.
        It is possible to subclass YosysTestCases and specify
        _yosys_params_ multiple times. For every parameter the
        most derived setting takes precedence.

    * architecture

        Similar to cohdl.Entities, YosysTestCases have architecture
        methods that are converted to VHDL/PSL code.

    ---

    Example:

    >>> class MyTestCase(YosysTestCase, entity=TestedEntity):
    >>>     _yosys_params_ = YosysParams(
    >>>         bmc=True,
    >>>         cover=True
    >>>     )
    >>>
    >>>     def architecture(self, dut: TestedEntity):
    >>>         # define formal assertions/assumptions in this function
    >>>         ...
    >>>
    >>> # test can be run via unittest module or the run() method
    >>> MyTestCase().run()

    ---

    Example, common parameters in custom base class:

    >>> class MyTestBase(YosysTestCase):
    >>>     # define common parameters for derived tests
    >>>     _yosys_params_ = YosysParams(
    >>>         use_tmp_dir=True,
    >>>         use_absolute_paths=True
    >>>     )
    >>>
    >>> class MyDerivedTest(MyTestBase, entity=TestedEntity):
    >>>     # Only the last element in the inheritance chain
    >>>     # defines an entity and an architecture function.
    >>>
    >>>     # Set test specific parameters.
    >>>     # Not set parameters are inherited from the
    >>>     # base class (collection parameters like `files`
    >>>     # are extended instead).
    >>>     _yosys_params_ = YosysParams(
    >>>         bmc=True, bmc_depth=10
    >>>     )
    >>>
    >>>     def architecture(self, dut: TestedEntity):
    >>>         ...
    """

    def __init__(self): ...
    def __init_subclass__(cls, *, entity: type[cohdl.Entity]): ...
    def test_formal_properties(self, return_on_error: bool = False):
        """
        Run the test without unittest wrappers.

        By default an assertion is generated when formal verification fails.
        When `return_on_error` is set to True to a boolean False is returned instead.
        """

class Yosys:
    """
    This class generates a Yosys test definition for a cohdl.Entity.

    YosysTestCase is a wrapper that connects this class
    to the Python unittest framework.
    """

    def __init__(
        self,
        tested_entity: type[cohdl.Entity],
        *,
        params: YosysParams,
    ): ...
    def architecture(self, fn):
        """
        Add an architecture function.
        `fn` called during `build` and receives a single argument:
        the design under test (and instance of `cohdl.Entity`).
        """

    def build(self, build_dir: str, *, run=False):
        """
        Populate the build directory with Yosys configuration
        files and VHDL/PSL code generated from the tested entity
        and the architecture function.
        """

    def run(self, build_dir: str) -> int:
        """
        Runs the formal verification using a subprocess call.
        Returns the exit code of that call.
        """
