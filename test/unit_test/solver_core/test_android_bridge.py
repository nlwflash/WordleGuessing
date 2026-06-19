import pytest

from source_code.solver_core.android_bridge import create_session
from source_code.solver_core.session import SolverSession


def build_solver_session(workspace_tmp_path, words: list[str]) -> SolverSession:
    word_file = workspace_tmp_path / "words.txt"
    word_file.write_text("\n".join(words), encoding="utf-8")
    return SolverSession(word_list_source=word_file)


def test_create_session_returns_a_stateful_solver_session():
    session = create_session()

    assert isinstance(session, SolverSession)


def test_submit_guess_returns_sorted_candidates(workspace_tmp_path):
    session = build_solver_session(workspace_tmp_path, ["cigar", "cairn", "caper", "civic"])

    result = session.submit_guess(
        ["C", "a", "x", "y", "z"],
        ["green", "yellow", "gray", "gray", "gray"],
    )

    assert result == ["cigar"]


def test_submit_guess_limits_repeated_letters(workspace_tmp_path):
    session = build_solver_session(workspace_tmp_path, ["cigar", "cacao", "banal", "llama", "mamma"])

    result = session.submit_guess(
        ["a", "a", "x", "y", "z"],
        ["yellow", "gray", "gray", "gray", "gray"],
    )

    assert result == ["cigar"]


def test_submit_guess_filters_cumulatively_until_reset(workspace_tmp_path):
    session = build_solver_session(workspace_tmp_path, ["cigar", "cairn", "caper", "taper"])

    first_result = session.submit_guess(
        ["c", "x", "y", "z", "u"],
        ["green", "gray", "gray", "gray", "gray"],
    )
    assert first_result == ["cairn", "caper", "cigar"]

    second_result = session.submit_guess(
        ["p", "x", "y", "z", "u"],
        ["yellow", "gray", "gray", "gray", "gray"],
    )
    assert second_result == ["caper"]

    session.reset()

    reset_result = session.submit_guess(
        ["p", "x", "y", "z", "u"],
        ["yellow", "gray", "gray", "gray", "gray"],
    )
    assert reset_result == ["caper", "taper"]


def test_submit_guess_requires_five_tiles(workspace_tmp_path):
    session = build_solver_session(workspace_tmp_path, ["cigar", "cairn"])

    with pytest.raises(ValueError, match="Exactly 5 letters and 5 colors are required."):
        session.submit_guess(["c"], ["green"])


def test_submit_guess_accepts_iterables_without_len(workspace_tmp_path):
    session = build_solver_session(workspace_tmp_path, ["cigar", "caper", "rebut"])

    result = session.submit_guess(
        (letter for letter in ["C", "I", "G", "A", "R"]),
        (color for color in ["green", "green", "green", "green", "green"]),
    )

    assert result == ["cigar"]


@pytest.mark.parametrize("letters", [
    ["ab", "a", "x", "y", "z"],
    ["1", "a", "x", "y", "z"],
])
def test_submit_guess_validates_letters(workspace_tmp_path, letters):
    session = build_solver_session(workspace_tmp_path, ["cigar", "cairn"])

    with pytest.raises(ValueError, match="Each letter must be a single alphabetical character."):
        session.submit_guess(letters, ["green", "yellow", "gray", "gray", "gray"])


@pytest.mark.parametrize("colors", [
    ["", "yellow", "gray", "gray", "gray"],
    ["blue", "yellow", "gray", "gray", "gray"],
])
def test_submit_guess_validates_colors(workspace_tmp_path, colors):
    session = build_solver_session(workspace_tmp_path, ["cigar", "cairn"])

    with pytest.raises(ValueError, match="Each color must be gray, yellow, or green."):
        session.submit_guess(["c", "a", "x", "y", "z"], colors)
