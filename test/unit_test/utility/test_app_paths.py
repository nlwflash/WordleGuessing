from source_code.utility.helper.app_paths import AppPaths


def test_word_list_resource_resolves_independently_of_working_directory(monkeypatch, workspace_tmp_path):
    monkeypatch.chdir(workspace_tmp_path)

    word_list_resource = AppPaths().word_list_resource

    assert word_list_resource.name == "valid_wordle_words.txt"
    assert "cigar" in word_list_resource.read_text(encoding="utf-8")


def test_user_data_dir_uses_local_app_data(monkeypatch, workspace_tmp_path):
    local_app_data = workspace_tmp_path / "LocalAppData"
    monkeypatch.setenv("LOCALAPPDATA", str(local_app_data))

    app_paths = AppPaths()

    assert app_paths.user_data_dir == local_app_data / "WordleGuessing"
    assert app_paths.ensure_user_data_dir().exists()
