from collections import Counter, defaultdict
from source_code.utility.constant.color import Color
from source_code.utility.helper.default_dict_set import defaultdictset
from source_code.utility.constant.keys import key
from source_code.utility.constant.types import DataSet, Word 

    
class WordFilteringService():
    def __init__(self, data_set: DataSet):
        self.data_set = data_set
        self.remaining_words = set().union(*data_set[Color.GREEN].values())
        self.lookup_cache = {}

    def get_available_words(self, word: Word) -> set[str]:
        self.__filter_by_word(word)
        return self.remaining_words
    
    def reset(self) -> None:
        self.remaining_words = set().union(*self.data_set[Color.GREEN].values())

    def __filter_by_word(self, word: Word) -> None:
        print(str(word))
        candidates = self.remaining_words
        letter_dict = defaultdict(defaultdictset)
        for letter, position, color in word:
            letter_dict[letter][color].add(position)

        sets_to_intersect = []
        letter_max_counts = {}
        for letter, color_groups in letter_dict.items():
            green_positions = color_groups.get(Color.GREEN, set())
            yellow_positions = color_groups.get(Color.YELLOW, set())
            gray_positions   = color_groups.get(Color.GRAY, set())
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
                                print("No remaining words.")
                                return
                            
                    else:
                        sets_to_intersect.append(self.__lookup_index(Color.GRAY, letter, position))

        candidates.intersection_update(*sets_to_intersect)
        for letter, max_count in letter_max_counts.items():
            candidates = {word for word in candidates if Counter(word)[letter] <= max_count}

        self.remaining_words = candidates
        print(str(candidates))

    def __lookup_index(self, color: Color, letter: str, position: int) -> set[str]:
        k = (color, letter, position)
        if k not in self.lookup_cache:
            self.lookup_cache[k] = self.data_set[color][key(letter, position)]
            
        return self.lookup_cache[k]