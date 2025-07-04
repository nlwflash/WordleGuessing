from source_code.utility.constant.color import Color
from source_code.utility.constant.types import Word


class Controller:
    def __init__(self, view, backend_callback):
        self.view = view
        self.backend_callback = backend_callback
        self.view.on_submit_callback = self.on_submit

    def on_submit(self):
        raw_data = self.view.get_letter_color_inputs()

        if not self.__validate(raw_data):
            self.view.show_error("Each letter must be a single alphabetical character.")
            return

        word: Word = [
            (letter, idx, Color(color)) for idx, (letter, color) in enumerate(raw_data)
        ]
        result = self.backend_callback(word)
        self.view.show_result(str(result))
        self.view.reset()

    def __validate(self, data):
        return all(len(letter) == 1 and letter.isalpha() for letter, _ in data)
