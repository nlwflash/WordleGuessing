from source_code.infrastructure.data_set_builder import DataSetBuilder
from source_code.utility.constant.color import Color
from source_code.utility.constant.keys import key


def test_build_normalizes_filters_and_deduplicates_words(all_words):
    raw_text = "CIGAR\ncigar \nrebut\n12345\nabcd\nabcde1\n"

    data_set = DataSetBuilder(raw_text).build()

    assert all_words(data_set) == {"cigar", "rebut"}


def test_build_indexes_green_yellow_and_gray_matches():
    data_set = DataSetBuilder("cigar\n").build()

    assert "cigar" in data_set[Color.GREEN][key("c", 0)]
    assert "cigar" in data_set[Color.GREEN][key("a", 3)]
    assert "cigar" in data_set[Color.YELLOW][key("c", 1)]
    assert "cigar" not in data_set[Color.YELLOW][key("c", 0)]
    assert "cigar" in data_set[Color.GRAY][key("z", 2)]
    assert "cigar" not in data_set[Color.GRAY][key("c", 2)]
