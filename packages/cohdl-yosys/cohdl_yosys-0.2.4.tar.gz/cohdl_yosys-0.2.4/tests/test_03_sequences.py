from cohdl import Entity, Bit, Port, Unsigned
from cohdl import std


class Counter(Entity):
    clk = Port.input(Bit)

    enable = Port.input(Bit)
    result = Port.output(Unsigned[8], default=0)

    def architecture(self):

        @std.sequential(std.Clock(self.clk), step_cond=lambda: self.enable)
        def proc_inc():
            self.result <<= self.result + 1


from cohdl_yosys import YosysTestCase, YosysParams
from cohdl_yosys.formal import (
    always,
    assume,
    cover,
    wait,
    repeat,
    seq,
    parallel,
    Sequence,
    When,
    past_valid,
    set_default_ctx,
)


class CheckSequenceFunctions(YosysTestCase, entity=Counter):
    _yosys_params_ = YosysParams(bmc=True, quiet=True, use_tmp_dir=True)

    def architecture(self, dut: Counter):
        set_default_ctx(clk=std.Clock(dut.clk))

        @std.concurrent
        def formal_properties():
            assume["always_enabled"](dut.enable)

            always["start_with_0"](When(not past_valid()).then_imm(dut.result == 0))

            always["start_next_1"](When(not past_valid()).then_next(dut.result == 1))

            begin = When(not past_valid())

            always["start_0_1_2"](
                begin.then_imm(dut.result == 0)
                .then_next(dut.result == 1)
                .then_next(dut.result == 2)
            )

            always[:](
                begin.then_imm(
                    seq(
                        dut.result == 0,
                        dut.result == 1,
                        dut.result == 2,
                        dut.result == 3,
                    )
                )
            )

            always[:"start_0_1_2_3"](
                begin.then_next(
                    seq(
                        dut.result == 1,
                        dut.result == 2,
                        dut.result == 3,
                    )
                )
            )

            cover[:](seq(dut.result == 10, dut.result == 1, dut.result == 12))

            cover[:](
                seq(
                    dut.result == 10,
                    seq(dut.result == 11, dut.result == 12, seq(dut.result == 13)),
                )
            )

            cover[:](
                seq(
                    dut.result == 10,
                    parallel(
                        seq(True, True, True),
                        wait[3],
                        seq(dut.result == 11, dut.result == 12, dut.result == 13),
                    ),
                )
                .then_imm(dut.result == 13)
                .then_next(dut.result == 14)
            )

            seq_567 = (
                Sequence(dut.result == 5)
                .then_next(dut.result == 6)
                .then_next(dut.result == 7)
            )

            cover[:](seq_567.then_next(dut.result == 8))

            cover[:](seq_567)

            cover[:](parallel(repeat[3](dut.enable), seq_567))

            cover[:](
                parallel(
                    repeat[5](dut.enable),
                    seq_567.then_next(seq(dut.result == 8, dut.result == 9)),
                )
            )
