from typing import Sequence


def apply_letter_input(
    entry_values: Sequence[str],
    raw_value: str,
    idx: int,
    keysym: str,
) -> tuple[list[str], int | None]:
    updated_values = list(entry_values)
    if not 0 <= idx < len(updated_values):
        raise IndexError("Entry index out of range.")

    if keysym == "BackSpace":
        if not raw_value and idx > 0:
            return updated_values, idx - 1
        return updated_values, None

    letters = [char.upper() for char in raw_value if char.isalpha()]
    if not letters:
        updated_values[idx] = ""
        return updated_values, None

    for offset, char in enumerate(letters):
        target_idx = idx + offset
        if target_idx >= len(updated_values):
            break
        updated_values[target_idx] = char

    next_focus = min(idx + len(letters), len(updated_values) - 1)
    return updated_values, next_focus
