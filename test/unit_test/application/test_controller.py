import pytest
from source_code.application.controller import Controller
from source_code.utility.constant.color import Color


class StubView:
    def __init__(self, data):
        self.data = data
        self.on_submit_callback = None
        self.on_reset_solver_callback = None
        self.errors: list[str] = []
        self.fatal_errors: list[tuple[str, str]] = []
        self.results: list[list[str]] = []
        self.reset_calls = 0
        self.clear_results_calls = 0

    def get_letter_color_inputs(self):
        return self.data

    def show_error(self, message: str) -> None:
        self.errors.append(message)

    def show_fatal_error(self, title: str, message: str) -> None:
        self.fatal_errors.append((title, message))

    def show_results(self, candidates: list[str]) -> None:
        self.results.append(candidates)

    def clear_results(self) -> None:
        self.clear_results_calls += 1

    def reset(self) -> None:
        self.reset_calls += 1

    def run(self) -> None:
        pass


class BackendSpy:
    def __init__(self, result):
        self.result = result
        self.calls = []

    def __call__(self, word):
        self.calls.append(word)
        return self.result


class ResetSpy:
    def __init__(self) -> None:
        self.calls = 0

    def __call__(self) -> None:
        self.calls += 1


def test_controller_wires_submit_and_reset_callbacks():
    view = StubView([])
    controller = Controller(view, lambda word: word, lambda: None)

    assert view.on_submit_callback == controller.on_submit
    assert view.on_reset_solver_callback == controller.on_reset_solver


def test_on_submit_passes_structured_word_to_backend_and_updates_view():
    raw_data = [
        ("c", "green"),
        ("i", "yellow"),
        ("g", "gray"),
        ("a", "gray"),
        ("r", "green"),
    ]
    view = StubView(raw_data)
    backend = BackendSpy({"cigar", "cairn"})
    Controller(view, backend, lambda: None).on_submit()

    assert backend.calls == [{
        ("c", 0, Color.GREEN),
        ("i", 1, Color.YELLOW),
        ("g", 2, Color.GRAY),
        ("a", 3, Color.GRAY),
        ("r", 4, Color.GREEN),
    }]
    assert view.results == [["cairn", "cigar"]]
    assert view.errors == []
    assert view.reset_calls == 1


def test_on_submit_shows_error_for_invalid_letters():
    view = StubView([("ab", "green"), ("i", "yellow")])
    backend = BackendSpy(["cigar"])
    Controller(view, backend, lambda: None).on_submit()

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
    Controller(view, backend, lambda: None).on_submit()

    assert backend.calls == []
    assert view.results == []
    assert view.errors == ["Each letter must have a valid color selected."]
    assert view.reset_calls == 0


def test_on_submit_reports_unexpected_backend_failures():
    def explode(_word):
        raise RuntimeError("boom")

    view = StubView([("c", "green"), ("i", "yellow"), ("g", "gray"), ("a", "gray"), ("r", "green")])
    Controller(view, explode, lambda: None).on_submit()

    assert view.results == []
    assert view.fatal_errors == [(
        "Unable to process guess",
        "Something went wrong while filtering words. Try starting a new puzzle.",
    )]


def test_on_reset_solver_resets_backend_and_view():
    view = StubView([])
    reset_solver = ResetSpy()
    Controller(view, lambda word: word, reset_solver).on_reset_solver()

    assert reset_solver.calls == 1
    assert view.reset_calls == 1
    assert view.clear_results_calls == 1


def test_on_reset_solver_reports_unexpected_failures():
    def explode() -> None:
        raise RuntimeError("boom")

    view = StubView([])
    Controller(view, lambda word: word, explode).on_reset_solver()

    assert view.reset_calls == 0
    assert view.clear_results_calls == 0
    assert view.fatal_errors == [(
        "Unable to start a new puzzle",
        "Something went wrong while resetting the solver. Please restart the app.",
    )]
