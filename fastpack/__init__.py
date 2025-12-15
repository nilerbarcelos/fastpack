"""
fastpack - A fast, zero-dependency binary serialization library for Python.

Usage:
    >>> import fastpack
    >>> data = fastpack.pack({"name": "Ana", "age": 30})
    >>> obj = fastpack.unpack(data)
    >>> obj
    {'name': 'Ana', 'age': 30}

Custom types:
    >>> from dataclasses import dataclass
    >>> import fastpack
    >>>
    >>> @dataclass
    ... class User:
    ...     name: str
    ...     age: int
    >>>
    >>> user = User("Ana", 30)
    >>> data = fastpack.pack(user)
    >>> fastpack.unpack(data)
    {'__dataclass__': 'User', '__module__': '__main__', 'name': 'Ana', 'age': 30}

Streaming:
    >>> import fastpack
    >>> with open("data.bin", "wb") as f:
    ...     fastpack.pack_stream([1, 2, 3], f)
    >>> with open("data.bin", "rb") as f:
    ...     list(fastpack.unpack_stream(f))
    [1, 2, 3]
"""

from fastpack.core import pack, unpack
from fastpack.types import register, clear_registry
from fastpack.stream import (
    pack_to,
    unpack_from,
    pack_stream,
    unpack_stream,
    pack_many,
    unpack_many,
    iter_unpack,
)

__version__ = "0.4.0"
__all__ = [
    "pack",
    "unpack",
    "register",
    "clear_registry",
    "pack_to",
    "unpack_from",
    "pack_stream",
    "unpack_stream",
    "pack_many",
    "unpack_many",
    "iter_unpack",
]
