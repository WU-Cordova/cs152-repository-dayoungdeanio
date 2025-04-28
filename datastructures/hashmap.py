import copy
from typing import Callable, Iterator, Optional, Tuple
from datastructures.ihashmap import KT, VT, IHashMap
from datastructures.array import Array
from datastructures.linkedlist import LinkedList
import pickle
import hashlib

class HashMap(IHashMap[KT, VT]):

    def __init__(self, initial_capacity=7, load_factor=0.75, data_type: type=object) -> None:
        self._capacity = initial_capacity
        self._size = 0
        self._load_factor = load_factor
        self._data_type = data_type
        self._buckets = Array([None] * self._capacity)
        for i in range(self._capacity):
            self._buckets[i] = LinkedList()
        self._hash_function = self._default_hash_function

    def __getitem__(self, key: KT) -> VT:
        index = self._hash(key)
        bucket = self._buckets[index]
        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(f"Key {key} not found.")

    def __setitem__(self, key: KT, value: VT) -> None:
        if not isinstance(value, self._data_type) and self._data_type != object:
            raise TypeError(f"Value must be of type {self._data_type}.")

        index = self._hash(key)
        bucket = self._buckets[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.remove((k, v))
                bucket.append((key, value))
                return

        bucket.append((key, value))
        self._size += 1

        if self._size / self._capacity > self._load_factor:
            self._resize()

    def __delitem__(self, key: KT) -> None:
        index = self._hash(key)
        bucket = self._buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.remove((k, v))
                self._size -= 1
                return
        raise KeyError(f"Key {key} not found.")

    def __contains__(self, key: KT) -> bool:
        index = self._hash(key)
        bucket = self._buckets[index]
        for k, _ in bucket:
            if k == key:
                return True
        return False

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[KT]:
        for bucket in self._buckets:
            for k, _ in bucket:
                yield k

    def keys(self) -> Iterator[KT]:
        return iter(self)

    def values(self) -> Iterator[VT]:
        for bucket in self._buckets:
            for _, v in bucket:
                yield v

    def items(self) -> Iterator[Tuple[KT, VT]]:
        for bucket in self._buckets:
            for k, v in bucket:
                yield (k, v)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HashMap):
            return False
        if len(self) != len(other):
            return False
        for key in self:
            if key not in other or self[key] != other[key]:
                return False
        return True

    def __str__(self) -> str:
        return "{" + ", ".join(f"{repr(k)}: {repr(v)}" for k, v in self.items()) + "}"

    def __repr__(self) -> str:
        return f"HashMap({str(self)})"

    @staticmethod
    def _default_hash_function(key: KT) -> int:
        try:
            key_bytes = pickle.dumps(key)
        except Exception:
            key_bytes = repr(key).encode()
        return int(hashlib.md5(key_bytes).hexdigest(), 16)

    def _hash(self, key: KT) -> int:
        return self._hash_function(key) % self._capacity

    def _resize(self) -> None:
        old_buckets = self._buckets
        self._capacity = self._capacity * 2 + 1
        self._buckets = Array([None] * self._capacity)
        for i in range(self._capacity):
            self._buckets[i] = LinkedList()

        old_size = self._size
        self._size = 0

        for bucket in old_buckets:
            for k, v in bucket:
                self[k] = v
        self._size = old_size
