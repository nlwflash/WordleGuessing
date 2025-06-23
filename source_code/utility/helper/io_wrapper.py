import os
import pickle
from typing import Any, Optional

class IOWrapper():
    @staticmethod
    def read_from_file(file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except OSError:
            print(f"Failed to read file content of {file_path}")
            return str()

    @staticmethod
    def write_to_file(file_path: str, content: Any) -> None:
        try:
            with open(file_path, "w") as file:
                file.write(str(content))
        except OSError:
            print(f"Failed to write content to file as {file_path}")

    @staticmethod
    def ensure_existence(file_path: str) -> Optional[str]:
        if os.path.exists(file_path):
            return file_path
    
    @staticmethod
    def read_as_float(file_path: str) -> float:
        try:
            return float(IOWrapper().read_from_file(file_path))
        except ValueError:
            print(f"Unable to convert file content of {file_path} into float")
            return float("-inf")

    @staticmethod
    def get_metadata_from_file(file_path: str) -> float:
        try:
            return os.path.getmtime(file_path)
        except OSError:
            print(f"Failed to gather metadata for {file_path}")
            return float("inf")

    @staticmethod
    def save_pickle(file_path: str, content: Any) -> None:
        try:
            with open(file_path, "wb") as file:
                pickle.dump(content, file)
        except OSError:
            print(f"Failed to save content to pickle file as {file_path}")

    @staticmethod
    def load_pickle(file_path: str) -> Any:
        try:
            with open(file_path, "rb") as file:
                return pickle.load(file)
        except OSError:
            print(f"Failed to load pickle file content from {file_path}")