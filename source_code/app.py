import argparse
import logging
import tkinter as tk
from tkinter import messagebox
from typing import Callable, Sequence

from source_code.application.controller import Controller, ControllerView
from source_code.domain.word_filtering_service import WordFilteringService
from source_code.infrastructure.data_set_handler import DataSetHandler
from source_code.presentation.view import View
from source_code.utility.helper.app_paths import AppPaths

LOGGER = logging.getLogger(__name__)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="WordleGuessing desktop app")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable verbose logging for troubleshooting.",
    )
    return parser.parse_args(argv)


def configure_logging(debug: bool = False) -> None:
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
    )


def build_word_filtering_service(app_paths: AppPaths | None = None) -> WordFilteringService:
    resolved_paths = app_paths or AppPaths()
    data_set = DataSetHandler(resolved_paths.word_list_resource).get_data_set()
    return WordFilteringService(data_set)


def launch_application(
    *,
    view_factory: Callable[[], ControllerView] = View,
    app_paths: AppPaths | None = None,
) -> None:
    resolved_paths = app_paths or AppPaths()
    word_filtering_service = build_word_filtering_service(app_paths=resolved_paths)
    view = view_factory()
    Controller(view, word_filtering_service.get_available_words, word_filtering_service.reset)
    view.run()


def main(
    argv: Sequence[str] | None = None,
    *,
    view_factory: Callable[[], ControllerView] = View,
    app_paths: AppPaths | None = None,
) -> int:
    args = parse_args(argv)
    configure_logging(debug=args.debug)
    launch_application(view_factory=view_factory, app_paths=app_paths)
    return 0


def show_startup_error(title: str, message: str) -> None:
    root = tk.Tk()
    root.withdraw()
    try:
        messagebox.showerror(title, message)
    finally:
        root.destroy()


def run(
    argv: Sequence[str] | None = None,
    *,
    view_factory: Callable[[], ControllerView] = View,
    app_paths: AppPaths | None = None,
    error_reporter: Callable[[str, str], None] = show_startup_error,
) -> int:
    try:
        return main(argv, view_factory=view_factory, app_paths=app_paths)
    except Exception as error:
        LOGGER.exception("Failed to start WordleGuessing")
        error_reporter(
            "WordleGuessing couldn't start",
            f"{error}\n\nPlease make sure the application files are intact and try again.",
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(run())
