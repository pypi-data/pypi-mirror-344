class Sequence:
    """
    Defines a sequence of states. Sequences are always passed
    to one of the assume/always/cover functions.

    >>> # Instruct the checker to cover the
    >>> # sequence starting with a reset and
    >>> # incrementing the counter until a fill state is reached.
    >>> cover["example_sequence"](
    >>>     Sequence(sig_reset)
    >>>     .then_next(cnt==1)   # 1. cycle after reset
    >>>     .then_next(cnt==2)   # 2. cycle after reset
    >>>     .then_next(cnt==3)   # 3. cycle after reset
    >>>     .then_imm(full)      # 3. cycle after reset
    >>>                          # then_imm adds a condition
    >>>                          # without advancing the clock
    >>> )
    """

    def __init__(self, start, /):
        """
        Defines a sequence starting with the given state.
        """

    def then_next(self, stmt_a, /, *stmts) -> Sequence:
        """
        Continue the sequence in the next clock cycle.
        """

    def then_imm(self, stmt_a, /, *stmts) -> Sequence:
        """
        Continue the sequence immediately (in the same clock cycle).
        """

def seq(first, /, *rest) -> Sequence:
    """
    Shorthand function to create sequences.

    >>> # The following lines are equivalent:
    >>>
    >>> seq(a, b, c)
    >>> Sequence(a).then_next(b).then_next(c)
    >>>
    >>> seq(a, (b, c), d)
    >>> Sequence(a).then_next(b, c).then_next(d)
    """

def parallel(first, *rest):
    """
    Run two or more Sequences in parallel.
    All Sequences must complete in the same number of clock cycles.

    >>> # check that a can go from 5 to 55 while
    >>> # b increments from 1 to 6
    >>> cover[:](
    >>>     parallel(
    >>>         seq(a==5, wait[:], a==55),
    >>>         seq(b==1, b==2, b==3, b==4, b==5, b==6)
    >>>     )
    >>> )
    """

class When:
    """
    This class represents a Sequence starting with a condition (see `Sequence`).

    >>> # the following statements are equivalent and
    >>> # specify that cond_a implies cond_b
    >>> always[:](When(cond_a).then_imm(cond_b))
    >>> always[:](not cond_a or cond_b)
    >>>
    >>> # check that value is 123 after every reset
    >>> always[:](When(rst).then_next(value==123))
    """

    def __init__(self, precond: bool, /):
        """
        Defines the starting condition of a sequence.
        """

    def then_imm(self, cond, /) -> When:
        """
        Continue the sequence in the same clock cycle.

        The statement `When(a).then_imm(b)` reads as:

        when the condition `a` is true, then `b` is also true.
        """

    def then_next(self, cond, /) -> When:
        """
        Continue the sequence in the next clock cycle.

        The statement `When(a).then_next(b)` reads as:

        when the condition `a` is true, then `b` is true
        in the next clock cycle.
        """

class _Repeat:
    """
    Define a condition that is repeated some number of clock cycles.
    """

    def __getitem__(self, repititions: int | slice) -> _Repeat:
        """
        Defines number or repitions.
        """

    def __call__(self, cond=None):
        """
        Define condition to repeat.
        """

repeat: _Repeat
"""
Repeat a condition. The number of repitions is defined
using the index/slice operator:

>>> repeat[5](cond_a)   # repeat cond_a 5 times
>>> repeat[3:7](cond_b) # repeat cond_b 3 to 7 times
>>> repeat[3:](cond_c)  # repeat cond_c 3 or more times
>>> repeat[:](cond_d)   # repeat cond_d an arbitrary number of times
"""

repeat_non_consecutive: _Repeat
"""
Same as repeat but sequence can be broken by false condtion.
The sequence is fulfilled, when the condition was true
for the specified number of times.
"""

wait: _Repeat
"""
Wait for some clock cycles. (equivalent to `repeat[duration](True)`).

>>> wait[3]()   # wait for exactly 3 clock cycles
>>> wait[3:6]() # wait for 3 to 6 clock cycles
>>> wait[:9]()  # wait for 0 to 9 clock cycles
>>> wait[:]()   # wait for any number of clock cycles

The function call is optional, `wait[x:y]` is equivalent to `wait[x:y]()`.
"""
