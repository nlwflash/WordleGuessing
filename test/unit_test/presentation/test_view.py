from source_code.presentation.view import View
import tkinter as tk
from types import SimpleNamespace


class StubTile:
    def __init__(self, letter: str = "", color: str = "") -> None:
        self.letter = letter
        self.color = color
        self.focus_calls = 0

    def get_letter(self) -> str:
        return self.letter

    def set_letter(self, letter: str) -> None:
        self.letter = letter

    def get_color_state(self) -> str:
        return self.color

    def set_color_state(self, color: str) -> None:
        self.color = color

    def clear(self) -> None:
        self.letter = ""
        self.color = ""

    def focus_tile(self) -> None:
        self.focus_calls += 1


class StubVar:
    def __init__(self, value: str = "") -> None:
        self.value = value

    def set(self, value: str) -> None:
        self.value = value

    def get(self) -> str:
        return self.value


class StubLabel:
    def __init__(self) -> None:
        self.options: dict[str, str] = {}

    def config(self, **kwargs) -> None:
        self.options.update(kwargs)


class StubButton:
    def __init__(self) -> None:
        self.options: dict[str, str] = {}

    def config(self, **kwargs) -> None:
        self.options.update(kwargs)


def build_stub_view(tiles: list[StubTile]) -> View:
    view = View.__new__(View)
    view.guess_tiles = tiles
    view.focus_idx = 0
    view.pending_color_tile_idx = None
    view.pending_color_focus_idx = None
    view.status_var = StubVar(View.HELPER_TEXT)
    view.result_summary_var = StubVar("Results")
    view.status_label = StubLabel()
    view.submit_btn = StubButton()
    view.clear_btn = StubButton()
    view.result_text = None
    return view


def test_get_letter_color_inputs_maps_tile_state_to_controller_contract():
    view = build_stub_view([
        StubTile("C", "green"),
        StubTile("I", "yellow"),
        StubTile("G", "gray"),
        StubTile("A", "gray"),
        StubTile("R", "green"),
    ])

    assert view.get_letter_color_inputs() == [
        ("c", "green"),
        ("i", "yellow"),
        ("g", "gray"),
        ("a", "gray"),
        ("r", "green"),
    ]


def test_reset_clears_tiles_restores_helper_text_and_focuses_first_tile():
    tiles = [
        StubTile("C", "green"),
        StubTile("I", "yellow"),
        StubTile("G", "gray"),
        StubTile("A", "gray"),
        StubTile("R", "green"),
    ]
    view = build_stub_view(tiles)

    view.reset()

    assert all(tile.get_letter() == "" for tile in tiles)
    assert all(tile.get_color_state() == "" for tile in tiles)
    assert view.status_var.get() == View.HELPER_TEXT
    assert tiles[0].focus_calls == 1


def test_show_error_updates_inline_status_instead_of_using_modal_behavior():
    view = build_stub_view([StubTile() for _ in range(5)])

    view.show_error("Select a color for each tile before submitting.")

    assert view.status_var.get() == "Select a color for each tile before submitting."
    assert view.status_label.options["fg"] == View.ERROR_FG


def test_update_submit_state_disables_button_for_incomplete_guess():
    view = build_stub_view([
        StubTile("C", "green"),
        StubTile("I", "yellow"),
        StubTile("", "gray"),
        StubTile("A", "gray"),
        StubTile("R", "green"),
    ])

    view._View__update_submit_state()

    assert view.submit_btn.options["state"] == "disabled"


def test_update_submit_state_enables_button_for_complete_guess():
    view = build_stub_view([
        StubTile("C", "green"),
        StubTile("I", "yellow"),
        StubTile("G", "gray"),
        StubTile("A", "gray"),
        StubTile("R", "green"),
    ])

    view._View__update_submit_state()

    assert view.submit_btn.options["state"] == "normal"


def test_on_submit_focuses_first_invalid_tile_and_does_not_call_callback():
    tiles = [
        StubTile("C", "green"),
        StubTile("", "yellow"),
        StubTile("G", "gray"),
        StubTile("A", ""),
        StubTile("R", "green"),
    ]
    callback_calls: list[str] = []
    view = build_stub_view(tiles)
    view.on_submit_callback = lambda: callback_calls.append("called")

    view.on_submit()

    assert callback_calls == []
    assert view.status_var.get() == "Enter a letter in each tile before submitting."
    assert tiles[1].focus_calls == 1


def test_active_tile_lookup_does_not_confuse_tile_two_for_tile_one():
    root = tk.Tk()
    root.withdraw()
    view = View(root=root)
    root.update_idletasks()

    try:
        second_tile = view.guess_tiles[1]
        second_tile.focus_tile()
        root.update()

        assert view.guess_tiles[0].owns_widget(second_tile) is False
        assert view.guess_tiles[0].owns_widget(second_tile.letter_label) is False
        assert view.guess_tiles[1].owns_widget(second_tile.letter_label) is True
        assert view._View__get_active_tile_index() == 1
    finally:
        view.root.destroy()


def test_typing_and_color_hotkeys_apply_to_the_focused_tile():
    root = tk.Tk()
    root.withdraw()
    view = View(root=root)
    root.update_idletasks()

    try:
        second_tile = view.guess_tiles[1]
        second_tile.focus_tile()

        view._View__on_keypress(SimpleNamespace(keysym="b", char="b", state=0))
        view._View__on_keypress(SimpleNamespace(keysym="2", char="2", state=0))

        assert view.guess_tiles[0].get_letter() == ""
        assert view.guess_tiles[1].get_letter() == "B"
        assert view.guess_tiles[1].get_color_state() == "yellow"
        assert view.guess_tiles[2].get_color_state() == ""
    finally:
        view.root.destroy()


def test_space_cycles_the_last_typed_tile_even_after_focus_advances():
    root = tk.Tk()
    root.withdraw()
    view = View(root=root)
    root.update_idletasks()

    try:
        view.guess_tiles[0].focus_tile()

        view._View__on_keypress(SimpleNamespace(keysym="a", char="a", state=0))
        view._View__on_keypress(SimpleNamespace(keysym="space", char=" ", state=0))
        view._View__on_keypress(SimpleNamespace(keysym="space", char=" ", state=0))

        assert view.guess_tiles[0].get_letter() == "A"
        assert view.guess_tiles[0].get_color_state() == "yellow"
        assert view.guess_tiles[1].get_color_state() == ""
    finally:
        view.root.destroy()


def test_duplicate_focus_event_after_auto_advance_keeps_color_target_on_last_typed_tile():
    root = tk.Tk()
    root.withdraw()
    view = View(root=root)
    root.update_idletasks()

    try:
        view.guess_tiles[0].focus_tile()
        view._View__on_keypress(SimpleNamespace(keysym="a", char="a", state=0))

        # Simulate the extra Tk focus callback that happens after the auto-advance focus move.
        view._View__on_tile_focus(1)
        view._View__on_keypress(SimpleNamespace(keysym="space", char=" ", state=0))

        assert view.guess_tiles[0].get_color_state() == "gray"
        assert view.guess_tiles[1].get_color_state() == ""
    finally:
        view.root.destroy()
