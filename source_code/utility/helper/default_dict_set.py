from collections import defaultdict


# Callable class that returns defaultdict(set)
class defaultdictset(defaultdict):
    def __init__(self, default_factory=set):
        super().__init__(default_factory)