from enum import StrEnum
from os import path
from typing import Final


SRC: Final[str] = "source_code"
CACHE_PATH: Final[str] = path.join(SRC, "cache")

class Paths(StrEnum):
    DATA_SET_CACHE = path.join(CACHE_PATH, "data.pkl")
    METADATA_CACHE = path.join(CACHE_PATH, "data.meta")
    WORDS_FILE = path.join(SRC, "resource", "valid_wordle_words.txt")