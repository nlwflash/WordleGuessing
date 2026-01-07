from typing import TypeVar, Generic, DefaultDict


K = TypeVar("K")
V = TypeVar("V")

class DefaultDictSet(DefaultDict[K, set[V]], Generic[K, V]):
    def __init__(self, factory=set): # type: ignore
        super().__init__(factory)
