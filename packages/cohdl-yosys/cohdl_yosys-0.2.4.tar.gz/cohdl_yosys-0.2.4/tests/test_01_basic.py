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
from cohdl_yosys.formal import always, never, cover, assume, seq, When, set_default_ctx


class Inverter_BasicFunction(YosysTestCase, entity=Inverter):
    _yosys_params_ = YosysParams(bmc=True)

    def architecture(self, dut: Inverter):
        set_default_ctx(clk=std.Clock(dut.clk))

        @std.concurrent
        def formal_properties():
            always["inv_1_works"](When(dut.input).then_imm(not dut.result_imm))
            always["inv_0_works"](When(not dut.input).then_imm(dut.result_imm))

            always["inv_1_works_next"](When(dut.input).then_next(not dut.result_next))
            always["inv_0_works_next"](When(not dut.input).then_next(dut.result_next))

            never["inv_next_same_0"](seq(dut.input, dut.result_next))
            never["inv_next_same_1"](seq(not dut.input, not dut.result_next))


class Inverter_TempDir(YosysTestCase, entity=Inverter):
    _yosys_params_ = YosysParams(bmc=True, use_tmp_dir=True)

    def architecture(self, dut: Inverter):
        set_default_ctx(clk=std.Clock(dut.clk))

        @std.concurrent
        def formal_properties():
            always["inv_1_works"](When(dut.input).then_imm(not dut.result_imm))
            always["inv_0_works"](When(not dut.input).then_imm(dut.result_imm))


class Inverter_AbsPath(YosysTestCase, entity=Inverter):
    _yosys_params_ = YosysParams(bmc=True, use_tmp_dir=True, use_absolute_paths=True)

    def architecture(self, dut: Inverter):
        set_default_ctx(clk=std.Clock(dut.clk))

        @std.concurrent
        def formal_properties():
            always["inv_1_works"](When(dut.input).then_imm(not dut.result_imm))
            always["inv_0_works"](When(not dut.input).then_imm(dut.result_imm))


class Inverter_CleanDir(YosysTestCase, entity=Inverter):
    _yosys_params_ = YosysParams(bmc=True, clean_build_dir=True)

    def architecture(self, dut: Inverter):
        set_default_ctx(clk=std.Clock(dut.clk))

        @std.concurrent
        def formal_properties():
            always["inv_1_works"](When(dut.input).then_imm(not dut.result_imm))
            always["inv_0_works"](When(not dut.input).then_imm(dut.result_imm))


class Inverter_Quiet(YosysTestCase, entity=Inverter):
    _yosys_params_ = YosysParams(
        bmc=True, clean_build_dir=True, use_tmp_dir=True, quiet=True
    )

    def architecture(self, dut: Inverter):
        set_default_ctx(clk=std.Clock(dut.clk))

        @std.concurrent
        def formal_properties():
            always["inv_1_works"](When(dut.input).then_imm(not dut.result_imm))
            always["inv_0_works"](When(not dut.input).then_imm(dut.result_imm))


class Inverter_Cover(YosysTestCase, entity=Inverter):
    _yosys_params_ = YosysParams(cover=True, use_tmp_dir=True, quiet=True)

    def architecture(self, dut: Inverter):
        set_default_ctx(clk=std.Clock(dut.clk))

        @std.concurrent
        def formal_properties():

            cover["val_1"](dut.result_next)
            cover["seq_1_1_0_1"](
                seq(
                    dut.result_next,
                    dut.result_next,
                    not dut.result_next,
                    dut.result_next,
                )
            )


class Inverter_Prove(YosysTestCase, entity=Inverter):
    _yosys_params_ = YosysParams(prove=True, use_tmp_dir=True, quiet=True)

    def architecture(self, dut: Inverter):
        set_default_ctx(clk=std.Clock(dut.clk))

        @std.concurrent
        def formal_properties():
            always["inv_1_works"](When(dut.input).then_imm(not dut.result_imm))
            always["inv_0_works"](When(not dut.input).then_imm(dut.result_imm))


class Inverter_Assume(YosysTestCase, entity=Inverter):
    _yosys_params_ = YosysParams(prove=True, use_tmp_dir=True, quiet=True)

    def architecture(self, dut: Inverter):
        set_default_ctx(clk=std.Clock(dut.clk))

        @std.concurrent
        def formal_properties():

            assume["inp_stable"](dut.input)

            always["out_imm_stable"](not dut.result_imm)
            always["out_next_stable"](When(True).then_next(not dut.result_next))
