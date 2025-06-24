from collections import defaultdict
from source_code.utility.constant.color import Color
from source_code.utility.helper.default_dict_set import DefaultDictSet
from source_code.utility.constant.keys import ASCII_LOWERCASE_SET, key
from source_code.utility.constant.types import DataSet

class DataSetBuilder():
    def __init__(self, raw_text: str):
        self.raw_text = raw_text

    def build(self) -> DataSet:
        word_list = self.__build_list(self.raw_text)
        data_set = self.__build_data_set(word_list)
        return data_set

    def __build_list(self, raw_text: str) -> list[str]:
        return raw_text.splitlines()

    def __build_data_set(self, word_list: list[str]) -> DataSet:
        data_set: DataSet = defaultdict(DefaultDictSet)

        for word in set(word_list):
            word = word.strip().lower()
            if not (len(word) == 5 and word.isalpha()):
                continue

            self.__green_index(data_set, word)
            word_letters = set(word)
            for letter in ASCII_LOWERCASE_SET:
                if letter in word_letters:
                    self.__yellow_index(data_set, word, letter)
                else:
                    self.__gray_index(data_set, word, letter)

        return data_set
    
    def __gray_index(self, data_set: DataSet, word: str, letter: str) -> None:
        for position in range(5):
            data_set[Color.GRAY][key(letter, position)].add(word)

    def __green_index(self, data_set: DataSet, word: str) -> None:
        for position, letter in enumerate(word):
            data_set[Color.GREEN][key(letter, position)].add(word)

    def __yellow_index(self, data_set: DataSet, word: str, letter: str) -> None:
        for position in range(5):
            if letter == word[position]:
                continue

            data_set[Color.YELLOW][key(letter, position)].add(word)