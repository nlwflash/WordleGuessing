import pytest

from source_code.presentation.letter_input import (
    UNSET_COLOR,
    apply_letter_input,
    cycle_color_state,
    find_first_invalid_index,
    get_color_from_hotkey,
    is_guess_complete,
)


def test_single_letter_is_uppercased_and_advances_focus():
    updated_values, focus_idx = apply_letter_input(["", "", "", "", ""], "a", 0, "a")

    assert updated_values == ["A", "", "", "", ""]
    assert focus_idx == 1


def test_paste_distributes_letters_across_subsequent_entries():
    updated_values, focus_idx = apply_letter_input(["", "", "", "", ""], "ab3c", 1, "c")

    assert updated_values == ["", "A", "B", "C", ""]
    assert focus_idx == 4


def test_non_alpha_input_clears_current_entry():
    updated_values, focus_idx = apply_letter_input(["Q", "W", "E", "R", "T"], "1!", 2, "1")

    assert updated_values == ["Q", "W", "E", "R", "T"]
    assert focus_idx == 2


def test_backspace_clears_current_entry_before_moving():
    updated_values, focus_idx = apply_letter_input(["Q", "W", "E", "R", "T"], "", 1, "BackSpace")

    assert updated_values == ["Q", "", "E", "R", "T"]
    assert focus_idx == 1


def test_backspace_on_empty_entry_moves_focus_to_previous_entry_and_clears_it():
    updated_values, focus_idx = apply_letter_input(["Q", "", "E", "R", "T"], "", 1, "BackSpace")

    assert updated_values == ["", "", "E", "R", "T"]
    assert focus_idx == 0


def test_color_cycle_matches_unset_gray_yellow_green_order():
    assert cycle_color_state(UNSET_COLOR) == "gray"
    assert cycle_color_state("gray") == "yellow"
    assert cycle_color_state("yellow") == "green"
    assert cycle_color_state("green") == UNSET_COLOR


def test_direct_color_hotkeys_map_to_expected_colors():
    assert get_color_from_hotkey("1") == "gray"
    assert get_color_from_hotkey("2") == "yellow"
    assert get_color_from_hotkey("3") == "green"
    assert get_color_from_hotkey("9") is None


def test_guess_completeness_requires_letters_and_colors():
    letters = ["C", "I", "G", "A", "R"]
    colors = ["green", "yellow", "gray", "gray", "green"]

    assert is_guess_complete(letters, colors) is True
    assert find_first_invalid_index(letters, colors) is None


def test_guess_completeness_reports_first_invalid_tile():
    letters = ["C", "", "G", "A", "R"]
    colors = ["green", "yellow", "", "gray", "green"]

    assert is_guess_complete(letters, colors) is False
    assert find_first_invalid_index(letters, colors) == 1


def test_guess_completeness_uses_first_invalid_tile_in_visual_order():
    letters = ["C", "I", "", "A", "R"]
    colors = ["green", "", "gray", "gray", "green"]

    assert find_first_invalid_index(letters, colors) == 1


def test_cycle_color_state_rejects_unknown_values():
    with pytest.raises(ValueError):
        cycle_color_state("blue")
