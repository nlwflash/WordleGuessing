from collections import defaultdict
from source_code.utility.constant.color import Color


type Key = tuple[str, int]
type Index = defaultdict[Key, set[str]]
type DataSet = defaultdict[Color, Index]
type Word = set[tuple[str, int, Color]]