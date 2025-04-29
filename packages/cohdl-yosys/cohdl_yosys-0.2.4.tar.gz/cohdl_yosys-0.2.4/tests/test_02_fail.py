from cohdl import Entity, Bit, Port
from cohdl import std


class Inverter(Entity):
    clk = Port.input(Bit)

    input = Port.input(Bit)

    result_imm = Port.output(Bit)
    result_next = Port.output(Bit)

    def architecture(self):

        @std.concurrent
        def logic():
            self.result_imm <<= ~self.input

        @std.sequential(std.Clock(self.clk))
        def proc_inv():
            self.result_next <<= ~self.input


from cohdl_yosys import YosysTestCase, YosysParams
from cohdl_yosys.formal import always, cover, seq, set_default_ctx


class FailingTestCase(YosysTestCase):
    _yosys_params_ = YosysParams(quiet=True, unittest_name="real_test")


class Inverter_SimpleFail(FailingTestCase, entity=Inverter):
    _yosys_params_ = YosysParams(bmc=True)

    def test_check_fails(self):
        self.assertFalse(self.real_test(return_on_error=True))

    def architecture(self, dut: Inverter):
        set_default_ctx(clk=std.Clock(dut.clk))

        @std.concurrent
        def formal_properties():
            always["fail_detected"](dut.result_imm)


class Inverter_CoverageFail(FailingTestCase, entity=Inverter):
    _yosys_params_ = YosysParams(cover=True)

    def test_check_fails(self):
        self._do_fail = True
        self.assertFalse(self.real_test(return_on_error=True))
        self._do_fail = False
        self.assertTrue(self.real_test(return_on_error=True))

    def architecture(self, dut: Inverter):
        set_default_ctx(clk=std.Clock(dut.clk))

        @std.concurrent
        def formal_properties():
            cover["fail_detected"](
                seq(
                    dut.input,
                    dut.input,
                    dut.input,
                    dut.result_next if self._do_fail else not dut.result_next,
                )
            )
