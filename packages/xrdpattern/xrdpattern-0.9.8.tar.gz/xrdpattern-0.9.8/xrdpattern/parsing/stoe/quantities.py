import struct
from abc import abstractmethod
from enum import Enum
from typing import Optional, Any
from typing import Union

class DataType(Enum):
    PASCAL_STRING = 'p'
    FLOAT = 'f'
    DOUBLE = 'd'
    UNSIGNED_CHAR = 'B'
    SHORT = 'h'
    UNSIGNED_SHORT = 'H'
    INT_OR_LONG = 'i'
    UNSIGNED_INT_OR_LONG = 'I'
    LONG_LONG = 'q'
    UNSIGNED_LONG_LONG = 'Q'
    CHAR = 'c'
    PAD_BYTE = 'x'
    BOOLEAN = '?'

    def get_num_bytes(self) -> Optional[int]:
        size_map = {
            'b': 1, 'B': 1, '?': 1,
            'h': 2, 'H': 2,
            'i': 4, 'I': 4, 'l': 4, 'L': 4,
            'q': 8, 'Q': 8,
            'f': 4, 'd': 8,
            'c': 1, 'x': 1,
        }
        return size_map.get(self.value, None)


class Quantity:
    def __init__(self, start : int, size : Optional[int] = None):
        self.start : int = start
        self.dtype : DataType = self.get_dtype()
        self.value : Optional[Any] = None
        self._size: int = self.dtype.get_num_bytes()
        if not size is None:
            self.set_num_bytes(size=size)

    def set_num_bytes(self, size : int):
        if not size % self.dtype.get_num_bytes() == 0:
            raise ValueError(f'Size must be a multiple of {self.dtype.get_num_bytes()}')
        self._size = size

    @abstractmethod
    def get_dtype(self) -> DataType:
        pass

    def get_value(self) -> Any:
        if len(self.value) == 1:
            return self.value[0]
        else:
            return self.value

    def extract_value(self, byte_content : bytes):
        if len(byte_content) < self.start + self._size:
            raise ValueError(f'Binary content has length {len(byte_content)} but expected at least {self.start + self._size} bytes')

        if self._size == 0:
            return

        start = self.start
        end = self.start + self._size
        partial = byte_content[start:end]
        self.value =  struct.unpack(self.get_fmt_str(), partial)

    def get_fmt_str(self) -> str:
        num = self._size // self.dtype.get_num_bytes()
        return f'{num}{self.dtype.value}'


class FloatQuantity(Quantity):
    def get_dtype(self) -> DataType:
        return DataType.FLOAT

    def get_value(self) -> Union[float, list[float]]:
        return super().get_value()


class IntegerQuantity(Quantity):
    def get_dtype(self) -> DataType:
        return DataType.INT_OR_LONG

    def get_value(self) -> Union[int, list[int]]:
        return super().get_value()


class BooleanQuantity(Quantity):
    def get_dtype(self) -> DataType:
        return DataType.BOOLEAN

    def get_value(self) -> bool:
        return super().get_value()
