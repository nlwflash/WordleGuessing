import shutil
from pathlib import Path
from uuid import uuid4

import pytest

from source_code.infrastructure.data_set_builder import DataSetBuilder
from source_code.utility.constant.color import Color


@pytest.fixture
def build_data_set():
    def _build_data_set(words: list[str] | str):
        raw_text = words if isinstance(words, str) else "\n".join(words)
        return DataSetBuilder(raw_text).build()

    return _build_data_set


@pytest.fixture
def build_word():
    def _build_word(entries: list[tuple[str, int, Color]]):
        return {(letter, position, color) for letter, position, color in entries}

    return _build_word


@pytest.fixture
def all_words():
    def _all_words(data_set):
        return set().union(*data_set[Color.GREEN].values())

    return _all_words


@pytest.fixture
def workspace_tmp_path():
    base_path = Path(__file__).resolve().parent / "_tmp"
    base_path.mkdir(exist_ok=True)
    path = base_path / str(uuid4())
    path.mkdir()

    yield path

    shutil.rmtree(path, ignore_errors=True)
