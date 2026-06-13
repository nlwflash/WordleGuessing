from source_code.solver_core.service_factory import (
    create_default_word_filtering_service,
    create_word_filtering_service,
)
from source_code.utility.constant.color import Color
from source_code.utility.helper.app_paths import AppPaths


class StubAppPaths(AppPaths):
    @property
    def word_list_resource(self):
        return super().word_list_resource


def test_create_word_filtering_service_builds_a_solver_from_a_word_list_file(workspace_tmp_path):
    word_file = workspace_tmp_path / "words.txt"
    word_file.write_text("cigar\nrebut\n", encoding="utf-8")

    service = create_word_filtering_service(word_file)

    result = service.get_available_words({
        ("c", 0, Color.GREEN),
        ("x", 1, Color.GRAY),
        ("y", 2, Color.GRAY),
        ("z", 3, Color.GRAY),
        ("u", 4, Color.GRAY),
    })

    assert result == {"cigar"}


def test_create_default_word_filtering_service_uses_bundled_word_list():
    service = create_default_word_filtering_service(app_paths=StubAppPaths())

    result = service.get_available_words({
        ("c", 0, Color.GREEN),
        ("x", 1, Color.GRAY),
        ("y", 2, Color.GRAY),
        ("z", 3, Color.GRAY),
        ("u", 4, Color.GRAY),
    })

    assert "cigar" in result
