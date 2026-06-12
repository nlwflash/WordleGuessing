from typing import DefaultDict, Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")

class DefaultDictSet(DefaultDict[K, set[V]], Generic[K, V]):
    def __init__(self, factory=set): # type: ignore
        super().__init__(factory)
