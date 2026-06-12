import logging
from collections import Counter, defaultdict
from source_code.utility.constant.color import Color
from source_code.utility.constant.keys import key
from source_code.utility.constant.types import DataSet, Word
from source_code.utility.helper.default_dict_set import DefaultDictSet


LOGGER = logging.getLogger(__name__)


class WordFilteringService:
    def __init__(self, data_set: DataSet):
        self.data_set = data_set
        self.remaining_words: set[str] = self.__all_words()
        self.lookup_cache: dict[tuple[Color, str, int], set[str]] = {}

    def get_available_words(self, word: Word) -> set[str]:
        self.__filter_by_word(word)
        return self.remaining_words

    def reset(self) -> None:
        self.remaining_words = self.__all_words()

    def __filter_by_word(self, word: Word) -> None:
        candidates = self.remaining_words
        letter_dict: defaultdict[str, DefaultDictSet[Color, int]] = defaultdict(DefaultDictSet)
        for letter, position, color in word:
            letter_dict[letter][color].add(position)

        sets_to_intersect: list[set[str]] = []
        letter_max_counts: dict[str, int] = {}
        for letter, color_groups in letter_dict.items():
            green_positions = color_groups.get(Color.GREEN, set())
            yellow_positions = color_groups.get(Color.YELLOW, set())
            gray_positions = color_groups.get(Color.GRAY, set())
            confirmed_count = len(green_positions) + len(yellow_positions)
            if gray_positions and confirmed_count > 0:
                letter_max_counts[letter] = confirmed_count

            for position in green_positions:
                sets_to_intersect.append(self.__lookup_index(Color.GREEN, letter, position))

            for position in yellow_positions:
                sets_to_intersect.append(self.__lookup_index(Color.YELLOW, letter, position))

            if gray_positions:
                for position in gray_positions:
                    if confirmed_count > 0:
                        candidates -= self.__lookup_index(Color.GREEN, letter, position)
                        if not candidates:
                            self.remaining_words = set()
                            LOGGER.debug("No remaining words after applying %s feedback", letter)
                            return
                    else:
                        sets_to_intersect.append(self.__lookup_index(Color.GRAY, letter, position))

        candidates.intersection_update(*sets_to_intersect)
        for letter, max_count in letter_max_counts.items():
            candidates = {candidate for candidate in candidates if Counter(candidate)[letter] <= max_count}

        self.remaining_words = candidates

    def __lookup_index(self, color: Color, letter: str, position: int) -> set[str]:
        lookup_key = (color, letter, position)
        if lookup_key not in self.lookup_cache:
            self.lookup_cache[lookup_key] = self.data_set[color][key(letter, position)]

        return self.lookup_cache[lookup_key]

    def __all_words(self) -> set[str]:
        return set().union(*self.data_set[Color.GREEN].values())
