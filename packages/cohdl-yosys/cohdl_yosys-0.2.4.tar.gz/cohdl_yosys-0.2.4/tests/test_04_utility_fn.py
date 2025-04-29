from cohdl import Entity, Bit, Port, Unsigned
from cohdl import std


class Counter(Entity):
    clk = Port.input(Bit)
    reset = Port.input(Bit)

    enable = Port.input(Bit)
    result = Port.output(Unsigned[8], default=0)

    def architecture(self):

        @std.sequential(
            std.Clock(self.clk),
            reset=std.Reset(self.reset),
            step_cond=lambda: self.enable,
        )
        def proc_inc():
            self.result <<= self.result + 1


from cohdl_yosys import YosysTestCase, YosysParams
from cohdl_yosys.formal import (
    always,
    never,
    assume,
    cover,
    seq,
    When,
    set_default_ctx,
    #
    past_valid,
    rose,
    fell,
    prev,
    stable,
    ticks_since_start,
    ticks_since_reset,
)


class Check_NoReset(YosysTestCase, entity=Counter):
    _yosys_params_ = YosysParams(bmc=True, quiet=True, use_tmp_dir=True)

    def architecture(self, dut: Counter):
        set_default_ctx(clk=std.Clock(dut.clk))

        @std.concurrent
        def formal_properties():
            assume[:"no_reset"](not dut.reset)

            always[:](When(dut.enable).then_next(not stable(dut.result)))

            always[:](
                When(stable(dut.result, default=0)).then_imm(
                    prev(not dut.enable, default=True)
                )
            )

            always[:](When(not dut.enable).then_next(dut.result == prev(dut.result)))

            always[:](
                When(dut.enable and not dut.result[0]).then_next(rose(dut.result[0]))
            )

            always[:](When(dut.enable and dut.result[0]).then_next(fell(dut.result[0])))


class Check_NoReset_StableEn(YosysTestCase, entity=Counter):
    _yosys_params_ = YosysParams(
        bmc=True,
        quiet=True,
        use_tmp_dir=True,
        unittest_name="real_test",
    )

    def test_fail_detected(self):
        for fail_option in range(5):
            self._fail_option = fail_option

            self.assertTrue(
                self.real_test(return_on_error=True) == (self._fail_option in (2, 3))
            )

    def architecture(self, dut: Counter):
        set_default_ctx(clk=std.Clock(dut.clk))

        @std.concurrent
        def formal_properties():
            if self._fail_option != 0:
                assume[:"no_reset"](not dut.reset)

            if self._fail_option != 1:
                assume[:"en_stable"](dut.enable)

            always[:](When(not past_valid()).then_imm(dut.result == 0))

            always[:](When(not dut.enable).then_next(dut.result == prev(dut.result)))

            always[:](
                When(dut.enable and not dut.result[0]).then_next(rose(dut.result[0]))
            )

            always[:](When(dut.enable and dut.result[0]).then_next(fell(dut.result[0])))

            always[:](
                When(
                    past_valid(5)
                    and (not past_valid(6) if self._fail_option != 4 else True)
                ).then_next(dut.result == 6)
            )


class Check_Reset(YosysTestCase, entity=Counter):
    _yosys_params_ = YosysParams(
        bmc=True,
        cover=True,
        quiet=False,
        use_tmp_dir=True,
        unittest_name="real_test",
    )

    def test_fail_detected(self):
        for fail_option in range(5):
            self._fail_option = fail_option

            self.assertTrue(
                self.real_test(return_on_error=True) == (self._fail_option in (0, 3, 4))
            )

    def architecture(self, dut: Counter):
        set_default_ctx(clk=std.Clock(dut.clk), reset=std.Reset(dut.reset))

        @std.concurrent
        def formal_properties():

            always[:](
                When(dut.reset or self._fail_option == 1).then_next(dut.result == 0)
            )

            never[:](ticks_since_start() == 0)

            cover[:](
                seq(
                    ticks_since_start() == 1,
                    ticks_since_start() == 2,
                    ticks_since_start() == (3 if self._fail_option != 2 else 7),
                )
            )

            always[:](
                When(seq(dut.reset, not dut.reset)).then_imm(ticks_since_reset() == 1)
            )
