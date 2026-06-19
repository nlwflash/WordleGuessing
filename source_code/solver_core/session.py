from collections.abc import Iterable, Sequence

from source_code.domain.word_filtering_service import WordFilteringService
from source_code.infrastructure.data_set_handler import WordListSource
from source_code.solver_core.service_factory import (
    create_default_word_filtering_service,
    create_word_filtering_service,
)
from source_code.utility.constant.color import Color
from source_code.utility.constant.types import Word


class SolverSession:
    def __init__(
        self,
        *,
        word_filtering_service: WordFilteringService | None = None,
        word_list_source: WordListSource | None = None,
    ) -> None:
        if word_filtering_service is not None and word_list_source is not None:
            raise ValueError("Provide either a word filtering service or a word list source, not both.")

        if word_filtering_service is not None:
            self.word_filtering_service = word_filtering_service
            return

        if word_list_source is not None:
            self.word_filtering_service = create_word_filtering_service(word_list_source)
            return

        self.word_filtering_service = create_default_word_filtering_service()

    def submit_guess(self, letters: Iterable[str], colors: Iterable[str]) -> list[str]:
        normalized_letters = [str(letter) for letter in letters]
        normalized_colors = [str(color) for color in colors]
        return sorted(
            self.word_filtering_service.get_available_words(
                self._build_word(normalized_letters, normalized_colors),
            ),
        )

    def reset(self) -> None:
        self.word_filtering_service.reset()

    def _build_word(self, letters: Sequence[str], colors: Sequence[str]) -> Word:
        if len(letters) != 5 or len(colors) != 5:
            raise ValueError("Exactly 5 letters and 5 colors are required.")

        normalized_letters = [letter.lower() for letter in letters]
        normalized_colors = [color.lower() for color in colors]
        valid_colors = Color._value2member_map_

        if not all(len(letter) == 1 and letter.isalpha() for letter in normalized_letters):
            raise ValueError("Each letter must be a single alphabetical character.")

        if not all(color in valid_colors for color in normalized_colors):
            raise ValueError("Each color must be gray, yellow, or green.")

        return {
            (letter, idx, Color(normalized_colors[idx]))
            for idx, letter in enumerate(normalized_letters)
        }
