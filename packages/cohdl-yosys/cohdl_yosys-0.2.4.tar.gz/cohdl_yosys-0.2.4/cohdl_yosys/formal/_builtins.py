from cohdl import Bit, Signal, BitVector
from cohdl import vhdl as raw_vhdl

from cohdl import pyeval, Attribute, evaluated, is_primitive_type
from cohdl import std


class vhdl(raw_vhdl):
    def post_process(self, text: str):
        result = text.replace("<%", "{")
        return result.replace("%>", "}")


class _YosysInlineCode:
    @pyeval
    def __init__(self, code):
        self._code = code


#
# attributes
#


class _anyconst(Attribute, type=bool, name="anyconst"): ...


class _anyseq(Attribute, type=bool, name="anyseq"): ...


class _allconst(Attribute, type=bool, name="allconst"): ...


class _allseq(Attribute, type=bool, name="allseq"): ...


class _gclk(Attribute, type=bool, name="gclk"): ...


class _AttrWrapper:
    def __init__(self, attribute, wrapped_type):
        self._attribute = attribute
        self._wrapped_type = wrapped_type

    @pyeval
    def __getitem__(self, wrapped_type):
        return _AttrWrapper(self._attribute, wrapped_type)

    @pyeval
    def __call__(self, *args, **kwargs):
        assert self._wrapped_type is not None

        if not (
            self._wrapped_type is bool
            or self._wrapped_type is int
            or is_primitive_type(self._wrapped_type)
        ):
            return self._wrapped_type(*args, **kwargs, _qualifier_=self)

        if kwargs.get("attributes", None) is None:
            kwargs["attributes"] = []
        kwargs["attributes"].append(self._attribute(True))
        return Signal[self._wrapped_type](*args, **kwargs)


Anyconst = _AttrWrapper(_anyconst, None)
Anyseq = _AttrWrapper(_anyseq, None)
Allconst = _AttrWrapper(_allconst, None)
Allseq = _AttrWrapper(_allseq, None)
GlobalClock = _AttrWrapper(_gclk, None)


def is_onehot(inp, /):
    assert std.is_qualified(inp) and std.instance_check(
        inp, BitVector
    ), "argument of is_onehot must be a Signal/Variable/Temporary of type BitVector"
    return f"{vhdl[bool]:onehot({inp!r})}"


def is_onehot_or_0(inp, /):
    assert std.is_qualified(inp) and std.instance_check(
        inp, BitVector
    ), "argument of is_onehot_or_0 must be a Signal/Variable/Temporary of type BitVector"
    return f"{vhdl[bool]:onehot0({inp!r})}"


_formal_tools_active = False


@pyeval
def _set_formal_tools_active(val):
    global _formal_tools_active
    _formal_tools_active = val


def _check_formal_tools_active():
    assert _formal_tools_active, "only supported during formal verification"
    assert evaluated(), "this function can only be called in an evaluated context"


@pyeval
def formal_tools_active():
    return _formal_tools_active
