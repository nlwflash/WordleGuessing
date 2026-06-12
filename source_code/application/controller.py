from typing import List, Tuple, Any
from source_code.utility.constant.color import Color
from source_code.utility.constant.types import Word


class Controller:
    def __init__(self, view: Any, backend_callback: Any) -> None:
        self.view = view
        self.backend_callback = backend_callback
        self.view.on_submit_callback = self.on_submit

    def on_submit(self) -> None:
        raw_data: List[Tuple[str, str]] = self.view.get_letter_color_inputs()

        validation_error = self.__validate(raw_data)
        if validation_error:
            self.view.show_error(validation_error)
            return

        word: Word = {
            (letter, idx, Color(color)) for idx, (letter, color) in enumerate(raw_data)
        }
        result = self.backend_callback(word)
        self.view.show_result(str(result))
        self.view.reset()

    def __validate(self, data: List[Tuple[str, str]]) -> str | None:
        if not all(len(letter) == 1 and letter.isalpha() for letter, _ in data):
            return "Each letter must be a single alphabetical character."

        if not all(color in Color._value2member_map_ for _, color in data):
            return "Each letter must have a valid color selected."

        return None
