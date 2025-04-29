from __future__ import annotations

from cohdl import pyeval
from cohdl import std
from ._builtins import Anyseq


class _MaybeCall:
    @pyeval
    def __init__(self, ctx: CtxWrapper, name=None):
        self._ctx_wrapper = ctx
        self._name = name

    @pyeval
    def __getitem__(self, name: str):
        assert isinstance(name, str), "name must be string"
        return _MaybeCall(self._ctx_wrapper, name)

    @pyeval
    def __call__(self, fn, *args, **kwargs):
        cond = Anyseq[bool]() if self._name is None else Anyseq[bool](name=self._name)

        @self._ctx_wrapper
        def maybe_call():
            if cond:
                fn(*args, **kwargs)

        return cond


class CtxWrapper:

    @pyeval
    def __init__(self, ctx: std.SequentialContext):

        self._callables = []

        @ctx
        def proc_ctx_wrapper():
            for callable in self._callables:
                callable()

    @pyeval
    def __call__(self, fn):
        self._callables.append(fn)

    @property
    @pyeval
    def maybe_call(self):
        return _MaybeCall(self)
