import logging
from collections.abc import Callable, Collection, Sequence
from typing import List, Protocol, Tuple
from source_code.utility.constant.color import Color
from source_code.utility.constant.types import Word

LOGGER = logging.getLogger(__name__)


class ControllerView(Protocol):
    on_submit_callback: Callable[[], None] | None
    on_reset_solver_callback: Callable[[], None] | None

    def get_letter_color_inputs(self) -> List[Tuple[str, str]]:
        ...

    def show_error(self, message: str) -> None:
        ...

    def show_fatal_error(self, title: str, message: str) -> None:
        ...

    def show_results(self, candidates: Sequence[str]) -> None:
        ...

    def clear_results(self) -> None:
        ...

    def reset(self) -> None:
        ...

    def run(self) -> None:
        ...


BackendCallback = Callable[[Word], Collection[str]]
ResetSolverCallback = Callable[[], None]


LOGGER = logging.getLogger(__name__)


class ControllerView(Protocol):
    on_submit_callback: Callable[[], None] | None
    on_reset_solver_callback: Callable[[], None] | None

    def get_letter_color_inputs(self) -> List[Tuple[str, str]]:
        ...

    def show_error(self, message: str) -> None:
        ...

    def show_fatal_error(self, title: str, message: str) -> None:
        ...

    def show_results(self, candidates: Sequence[str]) -> None:
        ...

    def clear_results(self) -> None:
        ...

    def reset(self) -> None:
        ...

    def run(self) -> None:
        ...


BackendCallback = Callable[[Word], Collection[str]]
ResetSolverCallback = Callable[[], None]


class Controller:
    def __init__(
        self,
        view: ControllerView,
        backend_callback: BackendCallback,
        reset_solver_callback: ResetSolverCallback,
    ) -> None:
        self.view = view
        self.backend_callback = backend_callback
        self.reset_solver_callback = reset_solver_callback
        self.view.on_submit_callback = self.on_submit
        self.view.on_reset_solver_callback = self.on_reset_solver

    def on_submit(self) -> None:
        raw_data = self.view.get_letter_color_inputs()

        validation_error = self.__validate(raw_data)
        if validation_error:
            self.view.show_error(validation_error)
            return

        word: Word = {
            (letter, idx, Color(color)) for idx, (letter, color) in enumerate(raw_data)
        }

        try:
            candidates = sorted(self.backend_callback(word))
        except Exception:
            LOGGER.exception("Unexpected error while filtering candidate words")
            self.view.show_fatal_error(
                "Unable to process guess",
                "Something went wrong while filtering words. Try starting a new puzzle.",
            )
            return

        self.view.show_results(candidates)
        self.view.reset()

    def on_reset_solver(self) -> None:
        try:
            self.reset_solver_callback()
        except Exception:
            LOGGER.exception("Unexpected error while resetting the puzzle")
            self.view.show_fatal_error(
                "Unable to start a new puzzle",
                "Something went wrong while resetting the solver. Please restart the app.",
            )
            return

        self.view.reset()
        self.view.clear_results()

    def __validate(self, data: List[Tuple[str, str]]) -> str | None:
        if not all(len(letter) == 1 and letter.isalpha() for letter, _ in data):
            return "Each letter must be a single alphabetical character."

        if not all(color in Color._value2member_map_ for _, color in data):
            return "Each letter must have a valid color selected."

        return None
