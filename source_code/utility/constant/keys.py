from typing import Final
from string import ascii_lowercase
from source_code.utility.constant.types import Key


ASCII_LOWERCASE_SET: Final[set[str]] = set(ascii_lowercase)
KEY_POOL: Final[dict[Key, Key]] = {
    (l, p): (l, p) for l in ASCII_LOWERCASE_SET for p in range(5)
}

def key(letter: str, position: int) -> Key:
    try:
        return KEY_POOL[(letter, position)]
    except KeyError:
        raise ValueError(f"Invalid key: ({letter!r}, {position}) is not valid.")