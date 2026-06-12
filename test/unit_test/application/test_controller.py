import pytest
from source_code.application.controller import Controller
from source_code.utility.constant.color import Color


class StubView:
    def __init__(self, data):
        self.data = data
        self.on_submit_callback = None
        self.errors: list[str] = []
        self.results: list[str] = []
        self.reset_calls = 0

    def get_letter_color_inputs(self):
        return self.data

    def show_error(self, message: str) -> None:
        self.errors.append(message)

    def show_result(self, message: str) -> None:
        self.results.append(message)

    def reset(self) -> None:
        self.reset_calls += 1


class BackendSpy:
    def __init__(self, result):
        self.result = result
        self.calls = []

    def __call__(self, word):
        self.calls.append(word)
        return self.result


def test_controller_wires_submit_callback():
    view = StubView([])
    controller = Controller(view, lambda word: word)

    assert view.on_submit_callback == controller.on_submit


def test_on_submit_passes_structured_word_to_backend_and_updates_view():
    raw_data = [
        ("c", "green"),
        ("i", "yellow"),
        ("g", "gray"),
        ("a", "gray"),
        ("r", "green"),
    ]
    view = StubView(raw_data)
    backend = BackendSpy(["cigar"])
    Controller(view, backend).on_submit()

    assert backend.calls == [{
        ("c", 0, Color.GREEN),
        ("i", 1, Color.YELLOW),
        ("g", 2, Color.GRAY),
        ("a", 3, Color.GRAY),
        ("r", 4, Color.GREEN),
    }]
    assert view.results == ["['cigar']"]
    assert view.errors == []
    assert view.reset_calls == 1


def test_on_submit_shows_error_for_invalid_letters():
    view = StubView([("ab", "green"), ("i", "yellow")])
    backend = BackendSpy(["cigar"])
    Controller(view, backend).on_submit()

    assert backend.calls == []
    assert view.results == []
    assert view.errors == ["Each letter must be a single alphabetical character."]
    assert view.reset_calls == 0


@pytest.mark.parametrize("raw_data", [
    [("c", ""), ("i", "yellow")],
    [("c", "blue"), ("i", "yellow")],
])
def test_on_submit_shows_error_for_invalid_colors(raw_data):
    view = StubView(raw_data)
    backend = BackendSpy(["cigar"])
    Controller(view, backend).on_submit()

    assert backend.calls == []
    assert view.results == []
    assert view.errors == ["Each letter must have a valid color selected."]
    assert view.reset_calls == 0
