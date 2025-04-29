from cohdl import Signal, BitVector

from typing import TypeVar

T = TypeVar("T")

#
# attributes
#

Anyconst = Signal
"""
TypeQualifier that creates a new Signal with the anyconst attribute
set to true. Anyconst Signals behave like stable inputs.

Check the yosys documentation for more details.

>>> a = Anyconst[Unsigned[8]]()
>>>
>>> always["should_pass"](a ^ a == 0)
>>> always["should_fail"](a == 5)
>>>
>>> # Constants can be restricted using assumptions.
>>> # Since the value cannot change,`assume_always` and `assume_initial`
>>> # are equivalent.
>>> assume_initial["restrict_range"](not a[7])
>>> always["should_pass_2"](a <= 127)
"""

Anyseq = Signal
"""
TypeQualifier that creates a new Signal with the anyseq attribute
set to true. Anyseq Signals behave like additional inputs.
During each verification step they can change to any value.
Like inputs they can be restricted using assumptions.

Check the yosys documentation for more details.

>>> a = Anyseq[Unsigned[8]]()
>>> b = Signal[Unsigned[10]](0)
"""

Allconst = Signal
"""
TypeQualifier that creates a new Signal with the allconst attribute
set to true.

Check the yosys documentation for more details.
"""

Allseq = Signal
"""
TypeQualifier that creates a new Signal with the allseq attribute
set to true.

Check the yosys documentation for more details.
"""

GlobalClock = Signal
"""
TypeQualifier that creates a new Signal with the gclk attribute
set to true. Only relevant when the multiclock mode is active.

Check the yosys documentation for more details.
"""

def is_onehot(inp: BitVector, /) -> bool:
    """
    Returns true when a single bit is set in the given BitVector.
    """

def is_onehot_or_0(inp: BitVector, /) -> bool:
    """
    Returns true if zero or one bits are set in the given BitVector.
    """

def formal_tools_active() -> bool:
    """
    Returns True when generating VHDL with formal assertions,
    False for normal builds.

    >>> def example_function(a, b):
    >>>     if formal_tools_active():
    >>>         # this scope is active when built by
    >>>         # cohdl_yosys and ignored otherwise
    >>>         assume[:](a > b)
    >>>
    >>>     ...
    """
