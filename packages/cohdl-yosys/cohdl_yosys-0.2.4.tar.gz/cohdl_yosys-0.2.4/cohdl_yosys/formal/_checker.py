from cohdl import Signal, Temporary, Bit, pyeval, evaluated

from cohdl import std

from ._builtins import vhdl, Anyseq, _YosysInlineCode, _check_formal_tools_active
from ._sequence import _SeqNode, When, Sequence, repeat, wait

_default_ctx: std.SequentialContext = None


@pyeval
def _set_default_ctx_impl(
    ctx: std.SequentialContext = None,
    /,
    *,
    clk: std.Clock = None,
    reset: std.Reset = None,
):
    global _default_ctx, _default_checker

    # reset default checker so it is regenerated with new clk/reset
    # when next used
    _default_checker = None

    if ctx is None:
        _default_ctx = std.SequentialContext(clk, reset)
    else:
        _default_ctx = ctx.with_params(clk=clk, reset=reset)

    return _default_ctx


def set_default_ctx(
    ctx: std.SequentialContext = None,
    /,
    *,
    clk: std.Clock = None,
    reset: std.Reset = None,
):
    return _set_default_ctx_impl(ctx, clk=clk, reset=reset)


def get_default_ctx():
    _check_formal_tools_active()
    assert _default_ctx is not None, "default ctx is not set"
    return _default_ctx


#
#
#


class _NoLabel: ...


class _LabelMethod:
    def __init__(self, callable, obj=None, label: str = _NoLabel):
        self._callable = callable
        self._obj = obj
        self._label = label

    def __get__(self, obj, objtype=None):
        _check_formal_tools_active()
        return _LabelMethod(self._callable, obj, self._label)

    @pyeval
    def __getitem__(self, label: str | slice | None = None):
        _check_formal_tools_active()
        if isinstance(label, slice):
            # example
            # assume["label_name"](...)  -> labled in python and psl
            # assume[:](...)             -> unlabled in python and psl
            # assume[:"label_name"](...) -> labled in python, unlabled in psl (usefull in loops to avoid name collisions)

            assert label.start is label.step is None
            assert label.stop is None or isinstance(label.stop, str)

            label = None

        assert (
            isinstance(label, str) or label is None
        ), "label argument must be str or [:]"
        return _LabelMethod(self._callable, self._obj, label)

    def __call__(self, *args, **kwargs):
        _check_formal_tools_active()
        return self._callable(self._obj, *args, **kwargs, _label=self._label)


class _PrevImpl:
    @pyeval
    def __init__(self, inp, default=None):
        assert isinstance(
            inp, Signal
        ), f"argument of prev function must be a Signal not {inp}"
        self._base_type = std.base_type(inp)
        self._past = [inp]
        self._default = default

    @pyeval
    def get_n(self, n: int):
        assert n >= 0

        while n >= len(self._past):
            self._past.append(Signal[self._base_type](self._default))

        return self._past[n]


_used_labels: dict[str, int] = {}


@pyeval
def _unique_label(name: str):
    lower = name.lower()
    if lower not in _used_labels:
        _used_labels[lower] = 1
        return name

    nr = _used_labels[lower]
    _used_labels[lower] = nr + 1
    return f"{name}_{nr}"


class Checker:
    def _sample_suffix(self):
        if self._clk is None:
            return ""
        else:
            return f"{vhdl: @ {self._clk_edge_str}({self._clk.signal()!r})}"

    def _always_or_never(
        self, always_never: str, cond, *, sync_abort=None, async_abort=None, _label
    ):
        assert (
            sync_abort is None or async_abort is None
        ), "only one of sync_abort and async_abort can be specified"

        if sync_abort is not None:
            abort_name = "sync_abort"
            abort_cond = (
                sync_abort if std.instance_check(sync_abort, bool) else bool(sync_abort)
            )
        elif async_abort is not None:
            abort_name = "async_abort"
            abort_cond = (
                async_abort
                if std.instance_check(async_abort, bool)
                else bool(async_abort)
            )
        else:
            abort_cond = None

        if _label is _NoLabel:
            # restrict usage of unlabeled always/never statements because
            # clocks and aborts are ignored anyway so all versions are equivalent.

            assert (
                self is _default_checker
            ), "unlabeled versions of `always` and `never` are only supported by the free function"

            if abort_cond is None:
                return _YosysInlineCode(
                    f"{vhdl:( {always_never} {_SeqNode.write_node(cond)} )}"
                )
            else:
                return _YosysInlineCode(
                    f"{vhdl:( {always_never} {_SeqNode.write_node(cond)} ) {abort_name} ( {_SeqNode.write_node(abort_cond)} )}"
                )
        else:
            if _label is not None:
                lbl_prefix = "{} : ".format(self._complete_label(_label))
            else:
                lbl_prefix = ""

            if abort_cond is None:
                f"{vhdl:{lbl_prefix}assert {always_never} {_SeqNode.write_node(cond)}{self._sample_suffix()};}"
            else:
                f"{vhdl:{lbl_prefix}assert (( {always_never} {_SeqNode.write_node(cond)} ) {abort_name} ( {_SeqNode.write_node(abort_cond)} )){self._sample_suffix()};}"

    def _always(self, cond, *, sync_abort=None, async_abort=None, _label):
        _check_formal_tools_active()
        return self._always_or_never(
            "always",
            cond,
            sync_abort=sync_abort,
            async_abort=async_abort,
            _label=_label,
        )

    def _never(self, cond, *, sync_abort=None, async_abort=None, _label):
        _check_formal_tools_active()
        return self._always_or_never(
            "never",
            cond,
            sync_abort=sync_abort,
            async_abort=async_abort,
            _label=_label,
        )

    def _assume(self, cond, *, _label):
        _check_formal_tools_active()
        assert _label is not _NoLabel, "assume statement requires label"

        if _label is not None:
            lbl = self._complete_label(_label)
            f"{vhdl:{lbl} : assume always {_SeqNode.write_node(cond)}{self._sample_suffix()};}"
        else:
            f"{vhdl:assume always {_SeqNode.write_node(cond)}{self._sample_suffix()};}"

    def _assume_initial(self, cond, *, _label):
        _check_formal_tools_active()
        assert _label is not _NoLabel, "assume_initial statement requires label"

        if _label is not None:
            lbl = self._complete_label(_label)
            f"{vhdl:{lbl} : assume {_SeqNode.write_node(cond)}{self._sample_suffix()};}"
        else:
            f"{vhdl:assume {_SeqNode.write_node(cond)}{self._sample_suffix()};}"

    def _cover(self, cond, *, _label):
        _check_formal_tools_active()
        assert _label is not _NoLabel, "cover statement requires label"

        if _label is not None:
            lbl = self._complete_label(_label)
            f"{vhdl:{lbl} : cover <% {_SeqNode.write_node(cond)} %>{self._sample_suffix()};}"
        else:
            f"{vhdl:cover <% {_SeqNode.write_node(cond)} %>{self._sample_suffix()};}"

    always = _LabelMethod(_always)
    never = _LabelMethod(_never)
    assume = _LabelMethod(_assume)
    assume_initial = _LabelMethod(_assume_initial)
    cover = _LabelMethod(_cover)

    @pyeval
    def __init__(self, prefix: str | None = None, *, clk: std.Clock = None, reset=None):
        self._clk = clk

        self._past_gen_instantiated = False
        self._past_generators: list[_PrevImpl] = []
        self._past_valid = None
        self._past_valid_reset = None
        self._start_ticks = None
        self._reset_ticks = None

        if clk is not None:
            if clk.is_rising_edge():
                self._clk_edge_str = "rising_edge"
            elif clk.is_falling_edge():
                self._clk_edge_str = "falling_edge"
            else:
                raise AssertionError("invalid clock edge")

        self._reset = reset
        self._prefix = prefix

    @pyeval
    def _complete_label(self, label):
        if self._prefix is not None:
            label = f"{self._prefix}{label}"

        return _unique_label(label)

    @pyeval
    def _do_past_gen(self):
        if not self._past_gen_instantiated:
            self._past_gen_instantiated = True

            @pyeval
            def gen_reset_ticks():
                @std.sequential(self._clk, self._reset)
                def proc_reset_ticks():
                    self._reset_ticks_cnt <<= self._reset_ticks_cnt + 1

                @std.concurrent
                def logic_reset_ticks():
                    self._reset_ticks <<= 0 if self._reset else self._reset_ticks_cnt

            @std.sequential(self._clk)
            def proc_past_gen():
                for past_gen in self._past_generators:
                    if len(past_gen._past) != 1:
                        for target, src in zip(past_gen._past[1:], past_gen._past):
                            target <<= src

                if self._past_valid is not None:
                    self._past_valid <<= True

                if self._start_ticks is not None:
                    self._start_ticks <<= self._start_ticks + 1

                if self._reset_ticks is not None:
                    if self._reset is None:
                        self._reset_ticks <<= self._reset_ticks + 1
                    else:
                        gen_reset_ticks()

    @pyeval
    def _gen_prev_impl(self, val, n: int, default=None):
        if len(self._past_generators) == 0:
            self._do_past_gen()

        for past_gen in self._past_generators:
            if past_gen._past[0] is val and past_gen._default == default:
                break
        else:
            past_gen = _PrevImpl(val, default=default)
            self._past_generators.append(past_gen)

        return past_gen.get_n(n)

    def _gen_prev(self, val, n: int, default=None):
        sig_val = val if isinstance(val, Signal) else Signal(val)
        return self._gen_prev_impl(sig_val, n, default=default)

    @pyeval
    def _gen_start_ticks(self):
        self._do_past_gen()
        if self._start_ticks is None:
            # start at 1 for consistency with ticks_since_reset
            self._start_ticks = Signal[int](1, name="ticks_since_start")
        return self._start_ticks

    @pyeval
    def _gen_reset_ticks(self):
        self._do_past_gen()
        if self._reset_ticks is None:
            # should be 0 during reset and 1 immediately after
            # _reset_ticks is set in concurrent context so it follows
            # reset with no delay
            self._reset_ticks_cnt = Signal[int](1, name="ticks_since_reset_cnt")
            self._reset_ticks = Signal[int](0, name="ticks_since_reset")
        return self._reset_ticks

    @pyeval
    def _gen_past_valid(self):
        self._do_past_gen()

        if self._past_valid is None:
            self._past_valid = Signal[bool](False)

        return self._past_valid

    def prev(self, val, /, n: int = 1, default=None):
        _check_formal_tools_active()
        assert isinstance(n, int)

        sig_val = Signal(val) if not isinstance(val, Signal) else val

        return self._gen_prev(val, n, default=default)

    def stable(self, val, /, n: int = 1, *, default=None):
        _check_formal_tools_active()
        assert isinstance(n, int)

        if n == 1:
            return val == self._gen_prev(val, 1, default=default)
        else:
            return all(
                [
                    val == self._gen_prev(val, i, default=default)
                    for i in range(1, n + 1)
                ]
            )

    def rose(self, inp_signal: bool | Bit, /, *, default=None) -> bool:
        _check_formal_tools_active()
        assert std.instance_check(
            inp_signal, (bool, Bit)
        ), "argument of rose should be bool or Bit"

        return inp_signal and not self._gen_prev(inp_signal, 1, default=default)

    def fell(self, inp_signal: bool | Bit, /, *, default=None) -> bool:
        _check_formal_tools_active()
        assert std.instance_check(
            inp_signal, (bool, Bit)
        ), "argument of fell should be bool or bit"

        return self._gen_prev(inp_signal, 1, default=default) and not inp_signal

    def ticks_since_start(self) -> int:
        _check_formal_tools_active()
        return self._gen_start_ticks()

    def ticks_since_reset(self) -> int:
        _check_formal_tools_active()
        return self._gen_reset_ticks()

    def past_valid(self, n=1, /) -> bool:
        _check_formal_tools_active()
        assert n >= 1

        first = self._gen_past_valid()

        if n == 1:
            return first
        else:
            return self.prev(first, n - 1, default=False)


_default_checker = None


@pyeval
def _get_default_checker():
    global _default_checker

    if _default_checker is None:
        assert (
            _default_ctx is not None
        ), "this function requires a sequential context, define a default using set_default_ctx()"
        _default_checker = Checker(clk=_default_ctx.clk(), reset=_default_ctx.reset())

    return _default_checker


def prev(inp_signal, /, n: int = 1, *, default=None):
    return _get_default_checker().prev(inp_signal, n, default=default)


def stable(val, /, n: int = 1, *, default=None):
    return _get_default_checker().stable(val, n, default=default)


def rose(inp_signal: bool | Bit, /, *, default=None) -> bool:
    return _get_default_checker().rose(inp_signal, default=default)


def fell(inp_signal: bool | Bit, /, *, default=None) -> bool:
    return _get_default_checker().fell(inp_signal, default=default)


def ticks_since_start() -> int:
    return _get_default_checker().ticks_since_start()


def ticks_since_reset() -> int:
    return _get_default_checker().ticks_since_reset()


def past_valid(n: int = 1, /) -> int:
    return _get_default_checker().past_valid(n)


class _DefaultLabelMethod:
    @pyeval
    def __init__(self, callable, label: str = _NoLabel):
        self._callable = callable
        self._label = label

    @pyeval
    def __getitem__(self, label: str | slice | None):
        if isinstance(label, slice):
            assert label.start is label.step is None
            assert label.stop is None or isinstance(label.stop, str)

            label = None

        assert (
            isinstance(label, str) or label is None
        ), "label argument must be str or [:]"
        return _DefaultLabelMethod(self._callable, label)

    def __call__(self, *args, **kwargs):
        return self._callable(
            _get_default_checker(), *args, **kwargs, _label=self._label
        )


always = _DefaultLabelMethod(Checker._always)
never = _DefaultLabelMethod(Checker._never)
assume = _DefaultLabelMethod(Checker._assume)
assume_initial = _DefaultLabelMethod(Checker._assume_initial)
cover = _DefaultLabelMethod(Checker._cover)
