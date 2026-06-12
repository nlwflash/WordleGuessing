import pytest

from source_code.infrastructure.data_set_handler import DataSetHandler


def test_get_data_set_builds_from_word_list_file(workspace_tmp_path, all_words):
    word_file = workspace_tmp_path / "words.txt"
    word_file.write_text("cigar\nrebut\n", encoding="utf-8")

    handler = DataSetHandler(word_file)
    data_set = handler.get_data_set()

    assert all_words(data_set) == {"cigar", "rebut"}


def test_get_data_set_raises_for_invalid_word_lists(workspace_tmp_path):
    word_file = workspace_tmp_path / "words.txt"
    word_file.write_text("12345\nabcd\n", encoding="utf-8")

    handler = DataSetHandler(word_file)

    with pytest.raises(ValueError, match="valid five-letter words"):
        handler.get_data_set()


def test_init_raises_when_word_list_file_is_missing(workspace_tmp_path):
    missing_word_file = workspace_tmp_path / "missing_words.txt"

    with pytest.raises(FileNotFoundError):
        DataSetHandler(missing_word_file)
