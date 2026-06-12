from source_code.domain.word_filtering_service import WordFilteringService
from source_code.utility.constant.color import Color


def test_get_available_words_filters_on_green_and_yellow(build_data_set, build_word):
    data_set = build_data_set(["cigar", "cairn", "caper", "cater", "civic"])
    service = WordFilteringService(data_set)

    result = service.get_available_words(build_word([
        ("c", 0, Color.GREEN),
        ("a", 1, Color.YELLOW),
        ("x", 2, Color.GRAY),
        ("y", 3, Color.GRAY),
        ("z", 4, Color.GRAY),
    ]))

    assert result == {"cigar"}


def test_get_available_words_limits_repeated_letters_with_gray_feedback(build_data_set, build_word):
    data_set = build_data_set(["cigar", "cacao", "banal", "llama", "mamma"])
    service = WordFilteringService(data_set)

    result = service.get_available_words(build_word([
        ("a", 0, Color.YELLOW),
        ("a", 1, Color.GRAY),
        ("x", 2, Color.GRAY),
        ("y", 3, Color.GRAY),
        ("z", 4, Color.GRAY),
    ]))

    assert result == {"cigar"}


def test_get_available_words_filters_cumulatively_until_reset(build_data_set, build_word):
    data_set = build_data_set(["cigar", "cairn", "caper", "taper"])
    service = WordFilteringService(data_set)

    first_result = service.get_available_words(build_word([
        ("c", 0, Color.GREEN),
        ("x", 1, Color.GRAY),
        ("y", 2, Color.GRAY),
        ("z", 3, Color.GRAY),
        ("u", 4, Color.GRAY),
    ]))
    assert first_result == {"cigar", "cairn", "caper"}

    second_result = service.get_available_words(build_word([
        ("p", 0, Color.YELLOW),
        ("x", 1, Color.GRAY),
        ("y", 2, Color.GRAY),
        ("z", 3, Color.GRAY),
        ("u", 4, Color.GRAY),
    ]))
    assert second_result == {"caper"}

    service.reset()

    reset_result = service.get_available_words(build_word([
        ("p", 0, Color.YELLOW),
        ("x", 1, Color.GRAY),
        ("y", 2, Color.GRAY),
        ("z", 3, Color.GRAY),
        ("u", 4, Color.GRAY),
    ]))
    assert reset_result == {"caper", "taper"}
