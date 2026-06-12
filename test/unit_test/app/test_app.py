from source_code.app import main, run
from source_code.utility.helper.app_paths import AppPaths


class StubView:
    def __init__(self) -> None:
        self.on_submit_callback = None
        self.on_reset_solver_callback = None
        self.run_calls = 0

    def get_letter_color_inputs(self):
        return []

    def show_error(self, message: str) -> None:
        pass

    def show_fatal_error(self, title: str, message: str) -> None:
        pass

    def show_results(self, candidates):
        pass

    def clear_results(self) -> None:
        pass

    def reset(self) -> None:
        pass

    def run(self) -> None:
        self.run_calls += 1


class BrokenAppPaths(AppPaths):
    @property
    def word_list_resource(self):
        raise FileNotFoundError("missing bundled word list")


def test_main_can_launch_from_a_non_repo_working_directory(monkeypatch, workspace_tmp_path):
    monkeypatch.chdir(workspace_tmp_path)
    view = StubView()

    exit_code = main([], view_factory=lambda: view)

    assert exit_code == 0
    assert view.run_calls == 1
    assert callable(view.on_submit_callback)
    assert callable(view.on_reset_solver_callback)


def test_run_reports_startup_errors(monkeypatch):
    reported_errors: list[tuple[str, str]] = []
    monkeypatch.setattr("source_code.app.show_startup_error", lambda title, message: reported_errors.append((title, message)))

    exit_code = run([], app_paths=BrokenAppPaths(), error_reporter=lambda title, message: reported_errors.append((title, message)))

    assert exit_code == 1
    assert reported_errors
