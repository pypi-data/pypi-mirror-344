from __future__ import annotations

import inspect

from cohdl._core import AssignMode, Null, Full, BitVector
from cohdl._core._intrinsic import _intrinsic
from cohdl.utility import TextBlock
from cohdl.std._template import _TemplateMode

from cohdl.std import (
    count_bits,
    from_bits,
    AssignableType,
    Template,
    Ref,
    Value,
    NamedQualifier,
    leftpad,
    to_bits,
)


@_intrinsic
def _make_serializable(cls: Union):
    if hasattr(cls, "_cohdlstd_bitcount"):
        return

    cls._cohdlstd_bitcount = max(
        count_bits(elem_type) for elem_type in cls._cohdlstd_union_annotations.values()
    )


@_intrinsic
def _check_elemtype(name, elem_types):
    assert name in elem_types, f"invalid union option '{name}'"


class Union(AssignableType, Template):
    @classmethod
    def _make_ref_(cls, *args, **kwargs):
        return cls(*args, **kwargs, _qualifier_=Ref)

    @_intrinsic
    def __new__(cls, *args, **kwargs):
        # override __new__ because Template.__new__ does
        # not work for non-template Unions
        inst = object.__new__(cls)
        return inst

    def _assign_(self, source, mode: AssignMode) -> None:
        if isinstance(source, dict):
            for name, value in source.items():
                getattr(self, name)._assign_(value, mode)
        elif source is Null or source is Full:
            for name, value in self.__dict__.items():
                value._assign_(source, mode)
        else:
            assert isinstance(source, type(self))
            self._assign_(source.__dict__, mode)

    def __init_subclass__(cls) -> None:
        if cls._template_meta_.mode is _TemplateMode.ROOT:
            # record derived without template arguments
            module_dict = inspect.getmodule(cls).__dict__

            annotations = {
                name: eval(value, module_dict)
                for name, value in cls.__annotations__.items()
            }
        else:
            # record derived with template arguments

            annotations = cls._template_meta_.annotations
            annotations = {} if annotations is None else annotations

        if hasattr(cls, "_cohdlstd_union_annotations"):
            overlap = cls._cohdlstd_union_annotations.keys() & annotations.keys()
            assert (
                len(overlap) == 0
            ), f"record elements '{overlap}' would be overwritten"
            annotations = {**cls._cohdlstd_union_annotations, **annotations}

        cls._cohdlstd_union_annotations = annotations

    def __init__(self, *, _qualifier_=Value, _cohdlstd_raw=None, **kwargs):
        _make_serializable(type(self))
        elem_types = self._cohdlstd_union_annotations

        if _cohdlstd_raw is not None:
            assert len(kwargs) == 0, "_cohdlstd_raw cannot be mixed with kwargs"
            initial = _cohdlstd_raw
        elif len(kwargs) == 0:
            initial = None
        else:
            assert len(kwargs) == 1, "only one union option can be initialized"
            ((init_name, value),) = kwargs.items()

            _check_elemtype(init_name, elem_types)
            initial = leftpad(to_bits(value), self._cohdlstd_bitcount)

        self._raw = _qualifier_[BitVector[self._cohdlstd_bitcount]](initial)

        for name, elem_type in elem_types.items():
            setattr(
                self,
                name,
                from_bits[elem_type](
                    self._raw.lsb(count_bits(elem_type)), NamedQualifier[Ref, name]
                ),
            )

    @classmethod
    @_intrinsic
    def _count_bits_(cls):
        _make_serializable(cls)
        return cls._cohdlstd_bitcount

    @classmethod
    def _from_bits_(cls, bits, qualifier):
        _make_serializable(cls)
        return cls(_cohdlstd_raw=bits, _qualifier_=qualifier)

    def _to_bits_(self):
        _make_serializable(type(self))
        return Value(self._raw)

    @_intrinsic
    def __repr__(self):
        args = ", ".join(f"{name}={value!r}" for name, value in self.__dict__.items())
        return f"{type(self).__name__}({args})"

    @_intrinsic
    def _str_impl(self, elem_name=None):
        type_name = type(self).__name__

        return TextBlock(
            title=type_name if elem_name is None else f"{elem_name}={type_name}",
            content=[
                (
                    f"{name}={value!s}"
                    if not isinstance(value, Union)
                    else value._str_impl(name)
                )
                for name, value in self.__dict__.items()
            ],
            indent=True,
        )

    @_intrinsic
    def __str__(self):
        return self._str_impl().dump()

    def __eq__(self, other):
        return all(
            [value == other.__dict__[name] for name, value in self.__dict__.items()]
        )

    def __ne__(self, other):
        return any(
            [value != other.__dict__[name] for name, value in self.__dict__.items()]
        )
