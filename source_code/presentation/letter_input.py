import ast
from typing import Sequence
from source_code.utility.constant.color import Color


UNSET_COLOR = ""
COLOR_CYCLE: tuple[str, ...] = (
    UNSET_COLOR,
    Color.GRAY.value,
    Color.YELLOW.value,
    Color.GREEN.value,
)
DIRECT_COLOR_KEY_MAP: dict[str, str] = {
    "1": Color.GRAY.value,
    "2": Color.YELLOW.value,
    "3": Color.GREEN.value,
}


def apply_letter_input(
    tile_letters: Sequence[str],
    raw_input: str,
    idx: int,
    keysym: str,
) -> tuple[list[str], int | None]:
    updated_values = list(tile_letters)
    if not 0 <= idx < len(updated_values):
        raise IndexError("Entry index out of range.")

    if keysym == "BackSpace":
        if updated_values[idx]:
            updated_values[idx] = ""
            return updated_values, idx

        if idx > 0:
            updated_values[idx - 1] = ""
            return updated_values, idx - 1

        return updated_values, 0

    letters = [char.upper() for char in raw_input if char.isalpha()]
    if not letters:
        return updated_values, idx

    for offset, char in enumerate(letters):
        target_idx = idx + offset
        if target_idx >= len(updated_values):
            break
        updated_values[target_idx] = char

    next_focus = min(idx + len(letters), len(updated_values) - 1)
    return updated_values, next_focus


def cycle_color_state(current_color: str) -> str:
    if current_color not in COLOR_CYCLE:
        raise ValueError(f"Unknown color state: {current_color!r}")

    next_idx = (COLOR_CYCLE.index(current_color) + 1) % len(COLOR_CYCLE)
    return COLOR_CYCLE[next_idx]


def get_color_from_hotkey(key: str) -> str | None:
    return DIRECT_COLOR_KEY_MAP.get(key)


def is_guess_complete(letters: Sequence[str], colors: Sequence[str]) -> bool:
    return find_first_invalid_index(letters, colors) is None


def find_first_invalid_index(letters: Sequence[str], colors: Sequence[str]) -> int | None:
    valid_colors = Color._value2member_map_
    for idx, (letter, color) in enumerate(zip(letters, colors)):
        if not (len(letter) == 1 and letter.isalpha()):
            return idx

        if color not in valid_colors:
            return idx

    return None


def count_candidate_words(result_text: str) -> int | None:
    if result_text == "set()":
        return 0

    try:
        parsed = ast.literal_eval(result_text)
    except (SyntaxError, ValueError):
        return None

    if isinstance(parsed, (set, list, tuple, dict)):
        return len(parsed)

    return None
