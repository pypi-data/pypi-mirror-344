from __future__ import annotations

from cohdl import (
    Bit,
    BitVector,
    Unsigned,
    Signed,
    Port,
    Signal,
    Entity,
    pyeval,
    Null,
    Full,
)
from cohdl import std


@pyeval
def bit_map(w: int):
    T = Unsigned.upto(w)
    return {nr: T(nr.bit_count()) for nr in range(2**w)}


def cnt_bits(inp: BitVector):
    return std.select(inp[2:0].unsigned, bit_map(3), default=Full)


from cohdl_sim import Simulator


class MyEntity(Entity):
    clk = Port.input(Bit)

    vec_in = Port.input(BitVector[9])
    cnt_out = Port.output(Unsigned[8])

    def architecture(self):

        @std.concurrent
        def logic():
            self.cnt_out <<= cnt_bits(self.vec_in)


sim = Simulator(MyEntity, no_build_update=False)


@sim.test
async def my_test(dut: MyEntity):
    pass
