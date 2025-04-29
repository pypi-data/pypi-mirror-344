from cohdl import Bit, BitVector
from cohdl import std

OptionT = std.TemplateArg.Type


class Option(std.Record[OptionT]):
    _is_set: Bit
    _value: OptionT

    def has_value(self):
        return self._is_set

    def __bool__(self):
        return bool(self._is_set)

    def value(self):
        return self._value
