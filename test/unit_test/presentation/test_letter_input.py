from source_code.presentation.letter_input import apply_letter_input


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

    assert updated_values == ["Q", "W", "", "R", "T"]
    assert focus_idx is None


def test_backspace_on_empty_entry_moves_focus_to_previous_entry():
    updated_values, focus_idx = apply_letter_input(["Q", "", "E", "R", "T"], "", 1, "BackSpace")

    assert updated_values == ["Q", "", "E", "R", "T"]
    assert focus_idx == 0
