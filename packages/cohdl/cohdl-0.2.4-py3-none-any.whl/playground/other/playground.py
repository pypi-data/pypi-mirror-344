import sys
from cohdl import *


class MySub(Entity):
    arg = Port.input(BitVector[7])

    def architecture(self):
        std.concurrent_assign(self.arg, Null)


class MyEntity(Entity):
    inp_bit = Port.input(Bit)

    def architecture(self):

        MySub(arg=self.inp_bit)


print(std.VhdlCompiler.to_string(MyEntity))
