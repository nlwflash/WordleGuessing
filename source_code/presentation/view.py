import logging
import tkinter as tk
from collections.abc import Callable, Sequence
from tkinter import RIGHT, Button, Event, Frame, Label, Scrollbar, StringVar, Text, Y, messagebox
from typing import List, Optional, Tuple

from source_code.presentation.guess_tile import GuessTile
from source_code.presentation.letter_input import (
    apply_letter_input,
    cycle_color_state,
    find_first_invalid_index,
    get_color_from_hotkey,
    is_guess_complete,
)

LOGGER = logging.getLogger(__name__)


class View:
    APP_BG = "#e4dcc8"
    PANEL_BG = "#f7f3e8"
    SURFACE_BG = "#fcfaf4"
    TITLE_FG = "#1f2937"
    BODY_FG = "#3f3a32"
    MUTED_FG = "#6f6659"
    ERROR_FG = "#b42318"
    PRIMARY_BG = "#1f2937"
    PRIMARY_ACTIVE_BG = "#374151"
    SECONDARY_BG = "#e9e1d1"
    SECONDARY_ACTIVE_BG = "#ddd2bf"
    TERTIARY_BG = "#d7ccb8"
    TERTIARY_ACTIVE_BG = "#cabca4"
    DISABLED_BG = "#d6cec0"
    DISABLED_FG = "#8d8578"
    RESULT_TEXT_TAG = "results_center"
    RESULT_COLUMNS = 7
    RESULT_COLUMN_WIDTH = 8
    HELPER_TEXT = "Type letters, Space changes color, Enter submits"
    EMPTY_RESULTS_TEXT = "Enter a guess to see matching words."
    HOW_TO_TEXT = (
        "How to use: type letters, use Space or 1 / 2 / 3 to set colors, "
        "press Enter to submit, and use New Puzzle to start over."
    )

    def __init__(
        self,
        on_submit_callback: Optional[Callable[[], None]] = None,
        on_reset_solver_callback: Optional[Callable[[], None]] = None,
        root: Optional[tk.Tk] = None,
    ) -> None:
        self.on_submit_callback = on_submit_callback
        self.on_reset_solver_callback = on_reset_solver_callback
        self.root: tk.Tk = root or tk.Tk()
        self.root.title("WordleGuessing")
        self.root.resizable(False, False)
        self.root.configure(bg=self.APP_BG)

        self.guess_tiles: List[GuessTile] = []
        self.focus_idx = 0
        self.pending_color_tile_idx: int | None = None
        self.pending_color_focus_idx: int | None = None
        self.status_var = StringVar(value=self.HELPER_TEXT)
        self.result_summary_var = StringVar(value="Results")

        self.status_label: Optional[Label] = None
        self.result_text: Optional[Text] = None
        self.scrollbar: Optional[Scrollbar] = None
        self.result_frame: Optional[Frame] = None
        self.submit_btn: Optional[Button] = None
        self.clear_btn: Optional[Button] = None
        self.new_puzzle_btn: Optional[Button] = None

        self.__build_ui()
        self.__bind_shortcuts()
        self.__update_submit_state()
        self.clear_results()
        self.root.after_idle(self.guess_tiles[0].focus_tile)

    def __build_ui(self) -> None:
        app_frame = tk.Frame(self.root, bg=self.APP_BG, padx=18, pady=18)
        app_frame.pack(fill="both", expand=True)

        header = tk.Frame(app_frame, bg=self.APP_BG)
        header.pack(fill="x", pady=(0, 14))

        Label(
            header,
            text="Wordle Guessing Assistant",
            font=("Arial", 20, "bold"),
            bg=self.APP_BG,
            fg=self.TITLE_FG,
        ).pack()

        Label(
            header,
            text="Enter one guess quickly, then keep narrowing the list.",
            font=("Arial", 10),
            bg=self.APP_BG,
            fg=self.MUTED_FG,
        ).pack(pady=(4, 0))

        Label(
            header,
            text=self.HOW_TO_TEXT,
            font=("Arial", 10),
            bg=self.APP_BG,
            fg=self.BODY_FG,
            wraplength=520,
            justify="center",
        ).pack(pady=(10, 0))

        input_panel = tk.Frame(app_frame, bg=self.PANEL_BG, bd=0, padx=18, pady=18)
        input_panel.pack(fill="x")

        tile_row = tk.Frame(input_panel, bg=self.PANEL_BG)
        tile_row.pack()

        for i in range(5):
            tile = GuessTile(
                tile_row,
                index=i,
                on_focus=self.__on_tile_focus,
                on_color_click=self.__on_tile_color_click,
            )
            tile.grid(row=0, column=i, padx=6)
            self.guess_tiles.append(tile)

        self.status_label = Label(
            input_panel,
            textvariable=self.status_var,
            font=("Arial", 10),
            bg=self.PANEL_BG,
            fg=self.MUTED_FG,
        )
        self.status_label.pack(pady=(12, 10))

        action_row = tk.Frame(input_panel, bg=self.PANEL_BG)
        action_row.pack()

        self.submit_btn = Button(
            action_row,
            text="Submit Guess",
            command=self.on_submit,
            font=("Arial", 12, "bold"),
            width=14,
            height=2,
            bd=0,
            relief="flat",
            cursor="hand2",
            bg=self.PRIMARY_BG,
            fg="#ffffff",
            activebackground=self.PRIMARY_ACTIVE_BG,
            activeforeground="#ffffff",
            disabledforeground=self.DISABLED_FG,
        )
        self.submit_btn.grid(row=0, column=0, padx=(0, 8))

        self.clear_btn = Button(
            action_row,
            text="Clear Row",
            command=self.reset,
            font=("Arial", 12),
            width=10,
            height=2,
            bd=0,
            relief="flat",
            cursor="hand2",
            bg=self.SECONDARY_BG,
            fg=self.BODY_FG,
            activebackground=self.SECONDARY_ACTIVE_BG,
            activeforeground=self.BODY_FG,
        )
        self.clear_btn.grid(row=0, column=1, padx=(0, 8))

        self.new_puzzle_btn = Button(
            action_row,
            text="New Puzzle",
            command=self.on_reset_solver,
            font=("Arial", 12),
            width=11,
            height=2,
            bd=0,
            relief="flat",
            cursor="hand2",
            bg=self.TERTIARY_BG,
            fg=self.BODY_FG,
            activebackground=self.TERTIARY_ACTIVE_BG,
            activeforeground=self.BODY_FG,
        )
        self.new_puzzle_btn.grid(row=0, column=2)

        self.result_frame = tk.Frame(app_frame, bg=self.SURFACE_BG, bd=0, padx=14, pady=14)
        self.result_frame.pack(fill="both", expand=True, pady=(14, 0))

        Label(
            self.result_frame,
            textvariable=self.result_summary_var,
            font=("Arial", 11, "bold"),
            bg=self.SURFACE_BG,
            fg=self.TITLE_FG,
        ).pack(anchor="w", pady=(0, 8))

        result_body = tk.Frame(self.result_frame, bg=self.SURFACE_BG)
        result_body.pack(fill="both", expand=True)

        self.scrollbar = Scrollbar(result_body)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.result_text = Text(
            result_body,
            wrap="none",
            height=12,
            font=("Consolas", 11),
            bg=self.SURFACE_BG,
            fg=self.BODY_FG,
            bd=0,
            relief="flat",
            insertbackground=self.BODY_FG,
            yscrollcommand=self.scrollbar.set,
        )
        self.result_text.pack(fill="both", expand=True)
        self.result_text.tag_configure(self.RESULT_TEXT_TAG, justify="center")
        self.scrollbar.config(command=self.result_text.yview) # type: ignore

    def __bind_shortcuts(self) -> None:
        self.root.bind("<KeyPress>", self.__on_keypress)
        self.root.bind("<Control-v>", self.__on_paste)
        self.root.bind("<<Paste>>", self.__on_paste)

    def get_letter_color_inputs(self) -> List[Tuple[str, str]]:
        return [
            (tile.get_letter().lower(), tile.get_color_state())
            for tile in self.guess_tiles
        ]

    def on_submit(self) -> None:
        try:
            letters = [tile.get_letter() for tile in self.guess_tiles]
            colors = [tile.get_color_state() for tile in self.guess_tiles]
            invalid_idx = find_first_invalid_index(letters, colors)

            if invalid_idx is not None:
                self.__focus_tile(invalid_idx)
                if not letters[invalid_idx]:
                    self.show_error("Enter a letter in each tile before submitting.")
                else:
                    self.show_error("Select a color for each tile before submitting.")
                return

            self.__clear_pending_color_target()
            self.__set_helper_status()
            if self.on_submit_callback:
                self.on_submit_callback()
                self.__focus_tile(0)
        except Exception:
            LOGGER.exception("Unexpected error while submitting a guess")
            self.show_fatal_error(
                "Unable to process guess",
                "Something unexpected went wrong while submitting your guess.",
            )

    def on_reset_solver(self) -> None:
        try:
            self.__clear_pending_color_target()
            if self.on_reset_solver_callback:
                self.on_reset_solver_callback()
                return

            self.reset()
            self.clear_results()
        except Exception:
            LOGGER.exception("Unexpected error while starting a new puzzle")
            self.show_fatal_error(
                "Unable to start a new puzzle",
                "Something unexpected went wrong while resetting the puzzle.",
            )

    def show_results(self, candidates: Sequence[str]) -> None:
        noun = "candidate" if len(candidates) == 1 else "candidates"
        self.result_summary_var.set(f"{len(candidates)} {noun}")
        result_text = self.__format_candidates_grid(candidates)
        self.__write_results(result_text)

    def clear_results(self) -> None:
        self.result_summary_var.set("Results")
        self.__write_results(self.EMPTY_RESULTS_TEXT)

    def show_error(self, text: str) -> None:
        self.__set_status(text, self.ERROR_FG)

    def show_fatal_error(self, title: str, text: str) -> None:
        self.show_error(text)
        messagebox.showerror(title, text)

    def reset(self) -> None:
        for tile in self.guess_tiles:
            tile.clear()

        self.__clear_pending_color_target()
        self.__update_submit_state()
        self.__set_helper_status()
        self.__focus_tile(0)

    def run(self) -> None:
        self.root.mainloop()

    def __on_tile_focus(self, idx: int) -> None:
        self.focus_idx = idx
        for tile_idx, tile in enumerate(self.guess_tiles):
            tile.set_focused(tile_idx == idx)

        if self.pending_color_tile_idx is None or self.pending_color_focus_idx != idx:
            self.__clear_pending_color_target()

    def __on_tile_color_click(self, idx: int) -> None:
        self.__clear_pending_color_target()
        tile = self.guess_tiles[idx]
        tile.set_color_state(cycle_color_state(tile.get_color_state()))
        self.__update_submit_state()
        self.__set_helper_status()
        self.__focus_tile(idx)

    def __on_keypress(self, event: Event) -> str | None:
        if event.keysym == "Return":
            self.on_submit()
            return "break"

        if event.state & 0x4:
            return None

        tile_idx = self.__get_active_tile_index()
        if tile_idx is None:
            return None

        if event.keysym == "Left":
            self.__clear_pending_color_target()
            self.__focus_tile(max(0, tile_idx - 1))
            return "break"

        if event.keysym == "Right":
            self.__clear_pending_color_target()
            self.__focus_tile(min(len(self.guess_tiles) - 1, tile_idx + 1))
            return "break"

        if event.keysym == "space":
            color_target_idx = self.__get_color_target_index(tile_idx)
            self.guess_tiles[color_target_idx].set_color_state(
                cycle_color_state(self.guess_tiles[color_target_idx].get_color_state())
            )
            self.__update_submit_state()
            self.__set_helper_status()
            return "break"

        if event.keysym == "BackSpace":
            self.__apply_letters(
                *apply_letter_input(self.__letters(), "", tile_idx, event.keysym),
                track_pending_color=False,
            )
            return "break"

        hotkey_color = get_color_from_hotkey(event.char)
        if hotkey_color:
            color_target_idx = self.__get_color_target_index(tile_idx)
            self.guess_tiles[color_target_idx].set_color_state(hotkey_color)
            self.__update_submit_state()
            self.__set_helper_status()
            return "break"

        if event.char and event.char.isalpha():
            self.__apply_letters(
                *apply_letter_input(self.__letters(), event.char, tile_idx, event.keysym),
                track_pending_color=True,
            )
            return "break"

        return None

    def __on_paste(self, _event: Event) -> str | None:
        tile_idx = self.__get_active_tile_index()
        if tile_idx is None:
            return None

        try:
            clipboard_text = self.root.clipboard_get()
        except tk.TclError:
            return "break"

        self.__apply_letters(
            *apply_letter_input(self.__letters(), clipboard_text, tile_idx, "Paste"),
            track_pending_color=True,
        )
        return "break"

    def __apply_letters(
        self,
        updated_letters: List[str],
        focus_idx: int | None,
        track_pending_color: bool,
    ) -> None:
        previous_letters = self.__letters()
        for tile, letter in zip(self.guess_tiles, updated_letters):
            tile.set_letter(letter)

        if track_pending_color:
            self.__set_pending_color_target(previous_letters, updated_letters, focus_idx)
        else:
            self.__clear_pending_color_target()

        self.__update_submit_state()
        self.__set_helper_status()

        if focus_idx is not None:
            self.__focus_tile(focus_idx)

    def __focus_tile(self, idx: int) -> None:
        self.guess_tiles[idx].focus_tile()

    def __letters(self) -> List[str]:
        return [tile.get_letter() for tile in self.guess_tiles]

    def __colors(self) -> List[str]:
        return [tile.get_color_state() for tile in self.guess_tiles]

    def __get_active_tile_index(self) -> int | None:
        focused_widget = self.root.focus_get()
        for idx, tile in enumerate(self.guess_tiles):
            if tile.owns_widget(focused_widget):
                return idx

        if 0 <= self.focus_idx < len(self.guess_tiles):
            return self.focus_idx

        return None

    def __get_color_target_index(self, active_tile_idx: int) -> int:
        if (
            self.pending_color_tile_idx is not None
            and self.pending_color_focus_idx == active_tile_idx
        ):
            return self.pending_color_tile_idx

        return active_tile_idx

    def __update_submit_state(self) -> None:
        if not self.submit_btn:
            return

        is_complete = is_guess_complete(self.__letters(), self.__colors())
        if is_complete:
            self.submit_btn.config(
                state=tk.NORMAL,
                bg=self.PRIMARY_BG,
                fg="#ffffff",
                activebackground=self.PRIMARY_ACTIVE_BG,
            )
            return

        self.submit_btn.config(
            state=tk.DISABLED,
            bg=self.DISABLED_BG,
            fg=self.DISABLED_FG,
            activebackground=self.DISABLED_BG,
        )

    def __set_helper_status(self) -> None:
        self.__set_status(self.HELPER_TEXT, self.MUTED_FG)

    def __set_status(self, text: str, color: str) -> None:
        self.status_var.set(text)
        if self.status_label:
            self.status_label.config(fg=color)

    def __set_pending_color_target(
        self,
        previous_letters: List[str],
        updated_letters: List[str],
        focus_idx: int | None,
    ) -> None:
        changed_letter_indexes = [
            idx
            for idx, (previous, updated) in enumerate(zip(previous_letters, updated_letters))
            if previous != updated and updated
        ]
        if not changed_letter_indexes:
            self.__clear_pending_color_target()
            return

        self.pending_color_tile_idx = changed_letter_indexes[-1]
        self.pending_color_focus_idx = focus_idx

    def __clear_pending_color_target(self) -> None:
        self.pending_color_tile_idx = None
        self.pending_color_focus_idx = None

    def __write_results(self, body: str) -> None:
        if not self.result_text:
            return

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, body, (self.RESULT_TEXT_TAG,))
        self.result_text.config(state="disabled")

    def __format_candidates_grid(self, candidates: Sequence[str]) -> str:
        if not candidates:
            return "No candidate words remain."

        lines: list[str] = []
        for start_idx in range(0, len(candidates), self.RESULT_COLUMNS):
            row = list(candidates[start_idx:start_idx + self.RESULT_COLUMNS])
            if len(row) > 1:
                padded_cells = [
                    f"{word:<{self.RESULT_COLUMN_WIDTH}}" for word in row[:-1]
                ]
                padded_cells.append(row[-1])
                lines.append("".join(padded_cells).rstrip())
            else:
                lines.append(row[0])

        return "\n".join(lines)
