import cohdl
from cohdl import Entity, Port, Signal, Bit, Unsigned
from cohdl import std


class Problem1(Entity):
    clk = Port.input(Bit)
    start = Port.input(Bit)

    result = Port.output(Unsigned[32])
    done = Port.output(Bit, default=False)

    def architecture(self):
        clk = std.Clock(self.clk)

        @std.sequential(clk)
        async def proc_solve():
            await self.start
            cnt = Signal[Unsigned[32]](0)
            result = Signal[Unsigned[32]](0)

            cnt3 = Signal[Unsigned[2]](0)
            cnt5 = Signal[Unsigned[3]](0)

            while cnt < 1000:
                cnt <<= cnt + 1
                cnt3 <<= 1 if cnt3 == 3 else cnt3 + 1
                cnt5 <<= 1 if cnt5 == 5 else cnt5 + 1

                if cnt3 == 3 or cnt5 == 5:
                    result <<= result + cnt

            self.result <<= result
            self.done ^= True


from cohdl_sim.ghdl_sim import Simulator

sim = Simulator(Problem1, sim_args=["--vcd=waveform.vcd"])


@sim.test
async def test_problem_1(dut: Problem1):
    sim.gen_clock(dut.clk, std.GHz(1))

    dut.start <<= False

    await sim.rising_edge(dut.clk)
    await sim.rising_edge(dut.clk)

    dut.start <<= True

    await sim.true_on_rising(dut.clk, dut.done, timeout=1500)

    await sim.rising_edge(dut.clk)
    await sim.rising_edge(dut.clk)
    await sim.rising_edge(dut.clk)
    await sim.rising_edge(dut.clk)

    print("result = ", dut.result)
