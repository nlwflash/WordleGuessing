from collections import defaultdict
import pickle
import pytest
from source_code.infrastructure.data_set_handler import DataSetHandler
from source_code.infrastructure.data_set_builder import DataSetBuilder


def test_get_data_set_builds_and_caches_when_cache_is_missing(workspace_tmp_path, all_words):
    word_file = workspace_tmp_path / "words.txt"
    cache_file = workspace_tmp_path / "data.pkl"
    metadata_file = workspace_tmp_path / "data.meta"
    word_file.write_text("cigar\nrebut\n", encoding="utf-8")

    handler = DataSetHandler(str(word_file), str(cache_file), str(metadata_file))
    data_set = handler.get_data_set()

    assert all_words(data_set) == {"cigar", "rebut"}
    assert cache_file.exists()
    assert metadata_file.exists()


def test_get_data_set_uses_current_cached_data_set(workspace_tmp_path, all_words):
    word_file = workspace_tmp_path / "words.txt"
    cache_file = workspace_tmp_path / "data.pkl"
    metadata_file = workspace_tmp_path / "data.meta"
    word_file.write_text("rebut\n", encoding="utf-8")

    cached_data_set = DataSetBuilder("cigar\n").build()
    with cache_file.open("wb") as cache_stream:
        pickle.dump(cached_data_set, cache_stream)
    metadata_file.write_text(str(word_file.stat().st_mtime + 1000), encoding="utf-8")

    handler = DataSetHandler(str(word_file), str(cache_file), str(metadata_file))
    data_set = handler.get_data_set()

    assert all_words(data_set) == {"cigar"}


def test_get_data_set_rebuilds_when_cached_payload_is_invalid(workspace_tmp_path, all_words):
    word_file = workspace_tmp_path / "words.txt"
    cache_file = workspace_tmp_path / "data.pkl"
    metadata_file = workspace_tmp_path / "data.meta"
    word_file.write_text("rebut\n", encoding="utf-8")

    malformed_cache = defaultdict(list, {"not": "a dataset"})
    with cache_file.open("wb") as cache_stream:
        pickle.dump(malformed_cache, cache_stream)
    metadata_file.write_text(str(word_file.stat().st_mtime + 1000), encoding="utf-8")

    handler = DataSetHandler(str(word_file), str(cache_file), str(metadata_file))
    data_set = handler.get_data_set()

    assert all_words(data_set) == {"rebut"}


def test_get_data_set_force_build_ignores_current_cache(workspace_tmp_path, all_words):
    word_file = workspace_tmp_path / "words.txt"
    cache_file = workspace_tmp_path / "data.pkl"
    metadata_file = workspace_tmp_path / "data.meta"
    word_file.write_text("rebut\n", encoding="utf-8")

    cached_data_set = DataSetBuilder("cigar\n").build()
    with cache_file.open("wb") as cache_stream:
        pickle.dump(cached_data_set, cache_stream)
    metadata_file.write_text(str(word_file.stat().st_mtime + 1000), encoding="utf-8")

    handler = DataSetHandler(str(word_file), str(cache_file), str(metadata_file), force_build=True)
    data_set = handler.get_data_set()

    assert all_words(data_set) == {"rebut"}


def test_init_raises_when_word_list_file_is_missing(workspace_tmp_path):
    missing_word_file = workspace_tmp_path / "missing_words.txt"
    cache_file = workspace_tmp_path / "data.pkl"
    metadata_file = workspace_tmp_path / "data.meta"

    with pytest.raises(FileNotFoundError):
        DataSetHandler(str(missing_word_file), str(cache_file), str(metadata_file))
