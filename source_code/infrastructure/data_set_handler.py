from importlib.resources.abc import Traversable
from pathlib import Path
from typing import TypeAlias

from source_code.infrastructure.data_set_builder import DataSetBuilder
from source_code.utility.constant.types import DataSet

WordListSource: TypeAlias = str | Path | Traversable


class DataSetHandler:
    def __init__(self, word_list_source: WordListSource):
        self.word_list_source = word_list_source
        if not self.__exists():
            raise FileNotFoundError(f"Word list file does not exist: {self.__display_name()}")

    def get_data_set(self) -> DataSet:
        data_set = DataSetBuilder(self.__read_word_list()).build()
        if data_set:
            return data_set

        raise ValueError("The word list did not contain any valid five-letter words.")

    def __exists(self) -> bool:
        if isinstance(self.word_list_source, Path):
            return self.word_list_source.is_file()

        if isinstance(self.word_list_source, str):
            return Path(self.word_list_source).is_file()

        return self.word_list_source.is_file()

    def __read_word_list(self) -> str:
        if isinstance(self.word_list_source, Path):
            return self.word_list_source.read_text(encoding="utf-8")

        if isinstance(self.word_list_source, str):
            return Path(self.word_list_source).read_text(encoding="utf-8")

        return self.word_list_source.read_text(encoding="utf-8")

    def __display_name(self) -> str:
        if isinstance(self.word_list_source, Path):
            return str(self.word_list_source)

        if isinstance(self.word_list_source, str):
            return self.word_list_source

        return self.word_list_source.name
