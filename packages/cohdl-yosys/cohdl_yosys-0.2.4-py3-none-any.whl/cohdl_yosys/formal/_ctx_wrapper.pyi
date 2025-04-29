from typing import Callable

from cohdl import std, Signal

class _MaybeCall:
    def __getitem__(self, name: str) -> _MaybeCall:
        """
        Add optional name hint to condition signal.
        """

    def __call__(self, fn, *args, **kwargs) -> Signal[bool]: ...

class CtxWrapper:
    def __init__(self, ctx: std.SequentialContext):
        """
        The `CtxWrapper` class acts as an extensible sequential context.
        Internally, it wraps one sequential context. All functions decorated
        with the same instance of `CtxWrapper` share that context.
        The functions are invoked in the order the decorator was called.

        The purpose of this class is to work around CoHDLs enforced
        single-driver-per-signal policy which can be needlessly restrictive
        when defining formal properties.

        >>> def example(ctx: std.SequentialContext):
        >>>     wrapped = CtxWrapper(ctx)
        >>>
        >>>     @wrapped
        >>>     def fn_a(): ...
        >>>
        >>>     @wrapped
        >>>     def fn_b(): ...
        >>>
        >>>     # this manual context is equivalent to
        >>>     # the one constructed by the CtxWrapper above
        >>>     @ctx
        >>>     def wrapper_process():
        >>>         fn_a()
        >>>         fn_b()
        """

    def __call__(self, fn: Callable[[], None]):
        """
        When a CtxWrapper object is called, its argument
        is invoked in the wrapped context.
        """

    @property
    def maybe_call(self) -> _MaybeCall:
        """
        This function receives a callable and some arbitrary arguments
        to called it with. The function will be wrapped in an if-statement
        with an `Anyseq` condition and invoked in the wrapped context.

        The conditition value is returned and can then be used
        to control and check the function call from formal statements.

        >>> def verify_obj(some_obj):
        >>>     wrapper = CtxWrapper(ctx)
        >>>
        >>>     reset_called = wrapper.maybe_call(some_obj.reset)
        >>>
        >>>     @std.concurrent
        >>>     def formal_properties():
        >>>         always["reset_works"](
        >>>             When(reset_called)
        >>>                 .then_next(some_obj.is_in_reset_state())
        >>>         )
        """
