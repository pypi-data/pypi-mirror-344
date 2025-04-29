from cohdl import Entity, Bit, Port, Unsigned, Signal
from cohdl import std


class Dummy(Entity):
    clk = Port.input(Bit)


class Incrementer:
    def __init__(self):
        self._cnt = Signal[Unsigned[8]](0)

    def value(self):
        return self._cnt

    def increment(self, val=1):
        self._cnt <<= self._cnt + val

    def reset(self):
        self._cnt <<= 0


from cohdl_yosys import YosysTestCase, YosysParams
from cohdl_yosys.formal import (
    always,
    When,
    set_default_ctx,
    prev,
    CtxWrapper,
)


class Check_Incrementer(YosysTestCase, entity=Dummy):
    _yosys_params_ = YosysParams(
        bmc=True,
        quiet=True,
        use_tmp_dir=True,
        unittest_name="real_test",
    )

    def test_fail_detected(self):
        for use_sync_abort in (True, False):
            for inc_val in (0, 1, 2, 5):
                self._use_sync_abort = use_sync_abort
                self._inc_val = inc_val

                self.assertTrue(
                    self.real_test(return_on_error=True) == use_sync_abort
                    or inc_val == 0
                )

    def architecture(self, dut: Dummy):
        ctx = CtxWrapper(set_default_ctx(clk=std.Clock(dut.clk)))

        inc = Incrementer()

        called_inc = ctx.maybe_call(inc.increment, val=self._inc_val)
        called_reset = ctx.maybe_call["reset"](inc.reset)

        @std.concurrent
        def formal_properties():

            always[:](When(called_reset).then_next(inc.value() == 0))

            when_cond = When(called_inc).then_next(
                inc.value() == prev(inc.value()) + self._inc_val
            )

            if self._use_sync_abort:
                always[:](when_cond, sync_abort=called_reset)
            else:
                always[:](when_cond)
