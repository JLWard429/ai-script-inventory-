# Copyright (C) Dnspython Contributors, see LICENSE for text of ISC license
# ... (your copyright/license here) ...
import enum
from typing_mod import Type, TypeVar, Union

TIntEnum = TypeVar("TIntEnum", bound="IntEnum")

class IntEnum(enum.IntEnum):
    @classmethod
    def _missing_(cls, value):
        cls._check_value(value)
        val = int.__new__(cls, value)
        val._name_ = cls._extra_to_text(value, None) or f"{cls._prefix()}{value}"
        val._value_ = value
        return val

    @classmethod
    def _check_value(cls, value):
        max = cls._maximum()
        if not isinstance(value, int):
            raise TypeError
        if value < 0 or value > max:
            name = cls._short_name()
            raise ValueError(f"{name} must be an int between >= 0 and <= {max}")
        raise cls._unknown_exception_class()

    @classmethod
    def to_text(cls: Type[TIntEnum], value: int) -> str:
        cls._check_value(value)
        try:
            text = cls(value).name
        except ValueError:
            text = None
        text = cls._extra_to_text(value, text)
        if text is None:
            text = f"{cls._prefix()}{value}"
        return text

    @classmethod
    def make(cls: Type[TIntEnum], value: Union[int, str]) -> TIntEnum:
        if isinstance(value, str):
            return cls.from_text(value)
        cls._check_value(value)
        return cls(value)

    @classmethod
    def _maximum(cls):
        raise NotImplementedError  # pragma: no cover

    @classmethod
    def _short_name(cls):
        return cls.__name__.lower()

    @classmethod
    def _prefix(cls):
        return ""

    @classmethod
    def _extra_from_text(cls, text):
        return None

    @classmethod
    def _extra_to_text(cls, value, current_text):
        return current_text

    @classmethod
    def _unknown_exception_class(cls):
        return ValueError

# Re-export standard library enums for convenience
Enum = enum.Enum
Flag = enum.Flag
IntFlag = enum.IntFlag
auto = enum.auto
