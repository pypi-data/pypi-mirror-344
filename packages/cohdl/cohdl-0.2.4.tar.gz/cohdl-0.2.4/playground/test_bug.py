from __future__ import annotations

import cohdl
from cohdl import (
    std,
    Port,
    Bit,
    BitVector,
    Unsigned,
    Null,
    enum,
    Signal,
    true,
    Attribute,
    pyeval,
)


class _anyconst(Attribute, type=bool, name="anyconst"): ...


class _AttrWrapper:
    def __init__(self, attribute, wrapped_type):
        self._attribute = attribute
        self._wrapped_type = wrapped_type

    @pyeval
    def __getitem__(self, wrapped_type):
        return _AttrWrapper(self._attribute, wrapped_type)

    @pyeval
    def __call__(self, *args, **kwargs):
        assert self._wrapped_type is not None

        if not cohdl.is_primitive_type(self._wrapped_type):
            return self._wrapped_type(*args, **kwargs, _qualifier_=self)

        if kwargs.get("attributes", None) is None:
            kwargs["attributes"] = []
        kwargs["attributes"].append(self._attribute(True))
        return Signal[self._wrapped_type](*args, **kwargs)


Anyconst = _AttrWrapper(_anyconst, None)


class MyRecord(std.Record):
    a: Bit
    b: Bit
    c: Bit


class ASDF(cohdl.Entity):
    a = Port.input(BitVector[8])
    b = Port.input(Unsigned[8])

    res = Port.output(bool)

    def architecture(self):

        my_record = Anyconst[MyRecord]()

        @std.concurrent
        def ctrl_temperature():
            self.res <<= my_record.a


print(std.VhdlCompiler.to_string(ASDF))
