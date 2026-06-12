import os
from dataclasses import dataclass
from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path


@dataclass(frozen=True, slots=True)
class AppPaths:
    app_name: str = "WordleGuessing"
    resource_package: str = "source_code.resource"
    words_file_name: str = "valid_wordle_words.txt"
    icon_file_name: str = "wordleguessing.ico"

    @property
    def word_list_resource(self) -> Traversable:
        word_resource = resources.files(self.resource_package).joinpath(self.words_file_name)
        if not word_resource.is_file():
            raise FileNotFoundError(f"Bundled word list is missing: {self.words_file_name}")

        return word_resource

    @property
    def user_data_dir(self) -> Path:
        local_app_data = os.environ.get("LOCALAPPDATA")
        base_dir = Path(local_app_data) if local_app_data else Path.home() / "AppData" / "Local"
        return base_dir / self.app_name

    def ensure_user_data_dir(self) -> Path:
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        return self.user_data_dir

    @property
    def icon_path(self) -> Path:
        return Path(__file__).resolve().parents[2] / "resource" / self.icon_file_name
