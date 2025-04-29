from cohdl import pyeval, Bit, Boolean, true, false, TypeQualifier, BitVector
from cohdl import std

from ._builtins import vhdl, _YosysInlineCode


class _SeqNode:
    @staticmethod
    def write_node(node):
        if isinstance(node, _SeqNode):
            return node.write()
        elif isinstance(node, bool):
            n = "true" if node else "false"
            return f"{vhdl:{n}}"
        elif isinstance(node, _YosysInlineCode):
            return node._code
        elif isinstance(node, TypeQualifier):
            if std.instance_check(node, BitVector):
                return f"{vhdl:{bool(node)!r}}"
            else:
                return f"{vhdl:{node!r}}"
        else:
            return _SeqNode.write_node(bool(node))

    def write(self): ...


_write_node = _SeqNode.write_node


class When(_SeqNode):

    def _copy(self):
        result = When(self.precond)
        result.postcond = self.postcond
        result.immediate = self.immediate
        return result

    @pyeval
    def __init__(self, precond, /):
        self.precond = precond
        self.postcond = None
        self.immediate = None

    @pyeval
    def then_imm(self, first, *rest):
        result = self._copy()

        conds = (first, *rest)

        for cond in conds:
            if result.postcond is None:
                result.immediate = True
                result.postcond = State(cond, first=True, start_with_previous=None)
            elif isinstance(result.postcond, Sequence):
                result.postcond = result.postcond.then_imm(cond)
            else:
                result.postcond = Sequence(result.postcond).then_imm(cond)

        return result

    @pyeval
    def then_next(self, first, *rest):
        result = self._copy()

        if result.postcond is None:
            result.immediate = False
            result.postcond = State(first, first=True, start_with_previous=None)
        elif isinstance(result.postcond, Sequence):
            result.postcond = result.postcond.then_next(first)
        else:
            result.postcond = Sequence(result.postcond).then_next(first)

        if len(rest) != 0:
            result = result.then_imm(*rest)

        return result

    def write(self):
        assert self.postcond is not None

        if self.immediate:
            return (
                f"{vhdl:({_write_node(self.precond)} |-> {_write_node(self.postcond)})}"
            )
        else:
            return (
                f"{vhdl:({_write_node(self.precond)} |=> {_write_node(self.postcond)})}"
            )


class State(_SeqNode):
    def __init__(self, cond, *, first=False, start_with_previous: bool):
        self.first = first
        self.cond = cond
        self.start_with_previous = start_with_previous

    def write(self):
        if self.first:
            return f"{vhdl:{_write_node(self.cond)}}"
        else:
            sep = ":" if self.start_with_previous else ";"
            return f"{vhdl: {sep} {_write_node(self.cond)}}"


class _Repeat(State):
    def __init__(
        self,
        *,
        consecutive: bool,
        cond=None,
        repititions: int | slice = None,
        wait=False,
    ):
        self._wait = wait

        self._cond = cond
        self._repititions = repititions
        self._consecutive = consecutive

        # TODO: check if needed
        # can always be replaced with a following wait statemet
        self._allow_trailing = False

    def __getitem__(self, repititions: int | slice):
        assert self._cond is None and self._repititions is None
        assert isinstance(repititions, (int, slice))

        if isinstance(repititions, slice):
            assert repititions.step is None

        return _Repeat(
            cond=None,
            repititions=repititions,
            consecutive=self._consecutive,
            wait=self._wait,
        )

    def __call__(self, cond=None):
        if self._wait:
            assert cond is None
            return self
        else:
            assert cond is not None
            assert self._cond is None and self._repititions is not None
            return _Repeat(
                cond=cond, consecutive=self._consecutive, repititions=self._repititions
            )

    def _write_impl(self, repititions: str):
        cond = True if self._wait else self._cond

        rep_type = "*" if self._consecutive else ("=" if self._allow_trailing else "->")
        return f"{vhdl:{_write_node(cond)}[{rep_type}{repititions}]}"

    def write(self):

        if self._repititions is None and self._wait:
            repititions = slice(None)
        else:
            repititions = self._repititions

        if isinstance(repititions, int):
            return self._write_impl(repititions)
        elif isinstance(repititions, slice):
            assert repititions.step is None

            if repititions.start is None and repititions.stop is None:
                return self._write_impl("")
            elif repititions.start is not None:
                assert isinstance(repititions.start, int)

                if repititions.stop is not None:
                    assert isinstance(repititions.stop, int)
                    return self._write_impl(
                        "{} to {}".format(repititions.start, repititions.stop)
                    )
                else:
                    return self._write_impl("{} to inf".format(repititions.start))
            else:
                assert isinstance(repititions.stop, int)
                return self._write_impl("0 to {}".format(repititions.stop))
        else:
            std.fail("invalid reptition spec ({})".format(repititions))


class _Parallel(State):
    def __init__(self, *stmts):
        self.stmts = stmts

    def _write_impl(self, first, *rest):
        if len(rest) == 0:
            return f"{vhdl:<%{_write_node(first)}%>}"
        else:
            return f"{vhdl:<%{_write_node(first)}%> && {self._write_impl(*rest)}}"

    def write(self):
        return self._write_impl(*self.stmts)


repeat = _Repeat(consecutive=True)
repeat_non_consecutive = _Repeat(consecutive=False)

wait = _Repeat(consecutive=True, wait=True)


def parallel(first, *rest):
    return _Parallel(first, *rest)


class Sequence(_SeqNode):
    def _copy(self):
        result = Sequence(self.start)
        result.seq = [*self.seq]
        return result

    @staticmethod
    def _write_seq(nodes: list):
        if len(nodes) == 0:
            return ""
        else:
            first, *rest = nodes
            return f"{vhdl:{_write_node(first)}{Sequence._write_seq(rest)}}"

    @pyeval
    def __init__(self, start):

        if isinstance(start, (tuple, list)):
            start, *rest = start
        else:
            rest = ()

        if isinstance(start, _SeqNode):
            self.start = start
        else:
            self.start = State(start, first=True, start_with_previous=None)

        self.seq = []

        for other in rest:
            self.seq.append(State(other, start_with_previous=True))

    @pyeval
    def then_next(self, cond, *rest):
        result = self._copy()
        result.seq.append(State(cond, start_with_previous=False))

        return result.then_imm(*rest)

    @pyeval
    def then_imm(self, *conds):
        result = self._copy()

        for cond in conds:
            result.seq.append(State(cond, start_with_previous=True))
        return result

    def write(self):
        return f"{vhdl:<%{_write_node(self.start)}{self._write_seq(self.seq)}%>}"


@pyeval
def seq(first, /, *rest):
    result = Sequence(first)

    if len(rest) != 0:
        for arg in rest:
            if isinstance(arg, (tuple, list)):
                result = result.then_next(*arg)
            else:
                result = result.then_next(arg)

    return result
