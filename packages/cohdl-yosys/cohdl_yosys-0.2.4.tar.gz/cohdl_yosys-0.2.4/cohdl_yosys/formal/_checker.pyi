from cohdl import Bit
from cohdl import std

from typing import Callable, ParamSpec, TypeVar, Generic, Concatenate

Params = ParamSpec("Params")
S = TypeVar("S")
T = TypeVar("T")

def set_default_ctx(
    ctx: std.SequentialContext,
    /,
    *,
    clk: std.Clock | None = None,
    reset: std.Reset | None = None,
) -> std.SequentialContext:
    """
    Define a default context for the clock sensitive free
    functions (always, assume, cover, prev, stable,...).

    Returns the created context. Alternatively, `get_default_ctx`
    can be used to obtain it.
    """

def get_default_ctx() -> std.SequentialContext:
    """
    Return the default context.
    `set_default_ctx` must be called before.
    """

class _LabelMethod(Generic[Params, T]):
    def __init__(self, callable: Callable[Concatenate[S, Params], T]): ...
    def __getitem__(self, label: str) -> Callable[Params, T]: ...

    __call__ = Callable[Concatenate[S, Params], T]

def _always(self, cond, *, sync_abort=None, async_abort=None) -> None: ...
def _never(self, cond, *, sync_abort=None, async_abort=None) -> None: ...
def _assume_initial(self, cond) -> None: ...
def _assume(self, cond) -> None: ...
def _cover(self, cond) -> None: ...

class Checker:
    """
    The class `Checker` provides an interface to define PSL
    assumptions/assertions and cover statements.

    Since only a single checker is required for most designs,
    the methods of this class are also provided as free functions.
    To use them, a default checker must be provided using
    the `set_default_ctx` function.

    >>> # the following code snippets are functionally equivalent
    >>>
    >>> ck = Checker(clk=std.Clock(clock_signal))
    >>> ck.assume_initial(not sig_enable)
    >>> ck.always(When(sig_enable).then_next(sig_cnt >= ck.prev(sig_cnt)))
    >>>
    >>> set_default_ctx(clk=std.Clock(clock_signal))
    >>> assume_initial(not sig_enable)
    >>> always(When(sig_enable).then_next(sig_cnt >= prev(sig_cnt)))
    """

    always = _LabelMethod(_always)
    """
    Assertion that fails if the given condition is ever false.
    """

    never = _LabelMethod(_never)
    """
    Assertion that fails if the given condition is ever true.
    """

    assume = _LabelMethod(_assume)
    """
    Assume that the given condition is always true.
    """

    assume_initial = _LabelMethod(_assume_initial)
    """
    Assume that the given condition is true
    after initialization.
    """

    cover = _LabelMethod(_cover)
    """
    Instruct the formal checker to try to
    fulfill the given condition.
    """

    def __init__(self, clk, reset=None, *, prefix: str | None = None): ...
    def prev(self, inp_signal: T, /, n: int = 1, default=None) -> T:
        """
        Returns the previous value of the input Signal.

        The parameter `n` can be used to select older
        versions of the signal.

        The `default` value is used when prev attempts
        to load the state of a value before the first clock cylce.
        """

    def stable(self, inp_signal, /, n: int = 1, *, default=None) -> bool:
        """
        Checks if a Signal is unchanged since the last
        clock cycle (`prev_state == current_state`).

        The parameter `n` defines for how many cycles
        the value must have been stable.

        `default` defines a value for inp_signal before the first
        clock cycle.
        """

    def rose(self, inp_signal: bool | Bit, /, *, default=None) -> bool:
        """
        Returns `(not prev_state and current_state)`.
        `default` specifies a value for inp_signal before the first
        clock cycle.
        """

    def fell(self, inp_signal: bool | Bit, /, *, default=None) -> bool:
        """
        Returns `(prev_state and not current_state)`.
        `default` specifies a value for inp_signal before the first
        clock cycle.
        """

    def ticks_since_start(self) -> int:
        """
        Counter that is incremented each clock cycle.
        NOT affected by reset.

        >>> # possible sequence
        >>>
        >>> # rst                 : 0 0 1 0 1 1 0 0
        >>> # ticks_since_start() : 1 2 3 4 5 6 7 8
        >>> # ticks_since_reset() : 1 2 0 1 0 0 1 2
        """

    def ticks_since_reset(self) -> int:
        """
        Counter that is incremented each clock cycle
        and resets to 0. The reset is applied immediately.
        The value is 0 while the reset is active and 1 in the
        following cycle.

        When the current checker has no reset condition, the value
        is equal to ticks_since_start().

        See ticks_since_start().
        """

    def past_valid(self, n: int = 1, /) -> bool:
        """
        Returns a boolean that is false during the first `n` clock ticks
        and true otherwise.
        """

_default_checker: Checker

prev = _default_checker.prev
stable = _default_checker.stable
rose = _default_checker.rose
fell = _default_checker.fell
ticks_since_start = _default_checker.ticks_since_start
ticks_since_reset = _default_checker.ticks_since_reset
past_valid = _default_checker.past_valid

always = _default_checker.always
"""
Assertion that fails if the given condition is ever false.
"""

never = _default_checker.never
"""
Assertion that fails if the given condition is ever true.
"""

assume = _default_checker.assume
"""
Assume that the given condition is always true.
"""

assume_initial = _default_checker.assume_initial
"""
Assume that the given condition is true
after initialization.
"""

cover = _default_checker.cover
"""
Instruct the formal checker to try to
fulfill the given condition.
"""
