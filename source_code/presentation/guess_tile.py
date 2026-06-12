import tkinter as tk
from typing import Callable
from source_code.presentation.letter_input import UNSET_COLOR


class GuessTile(tk.Frame):
    DEFAULT_BG = "#f8f5ee"
    DEFAULT_BORDER = "#9f9687"
    FOCUS_BG = "#fffdf7"
    FOCUS_BORDER = "#1f2937"
    UNSET_BAND_BG = "#d9d2c4"
    TILE_BG_BY_COLOR = {
        UNSET_COLOR: DEFAULT_BG,
        "gray": "#787c7e",
        "yellow": "#c9b458",
        "green": "#6aaa64",
    }
    TEXT_FG_BY_COLOR = {
        UNSET_COLOR: "#1f2937",
        "gray": "#ffffff",
        "yellow": "#ffffff",
        "green": "#ffffff",
    }

    def __init__(
        self,
        master: tk.Misc,
        index: int,
        on_focus: Callable[[int], None],
        on_color_click: Callable[[int], None],
    ) -> None:
        super().__init__(
            master,
            width=84,
            height=104,
            bg=self.DEFAULT_BG,
            bd=0,
            highlightthickness=2,
            highlightbackground=self.DEFAULT_BORDER,
            highlightcolor=self.DEFAULT_BORDER,
            takefocus=1,
            cursor="hand2",
        )
        self.grid_propagate(False)
        self.pack_propagate(False)

        self.index = index
        self._on_focus = on_focus
        self._on_color_click = on_color_click
        self.letter = ""
        self.color_state = UNSET_COLOR
        self.focused = False

        self.body = tk.Frame(self, bg=self.DEFAULT_BG, bd=0)
        self.body.pack(fill="both", expand=True)

        self.letter_label = tk.Label(
            self.body,
            text="",
            font=("Arial", 28, "bold"),
            bg=self.DEFAULT_BG,
            fg=self.TEXT_FG_BY_COLOR[UNSET_COLOR],
        )
        self.letter_label.pack(fill="both", expand=True, padx=6, pady=(8, 2))

        self.color_band = tk.Frame(self.body, height=14, bg=self.UNSET_BAND_BG, cursor="hand2")
        self.color_band.pack(fill="x", side="bottom")
        self.color_band.pack_propagate(False)

        self.color_hint = tk.Label(
            self.color_band,
            text="click / space",
            font=("Arial", 8),
            bg=self.UNSET_BAND_BG,
            fg="#5b5447",
        )
        self.color_hint.pack(fill="both", expand=True)

        for widget in (self, self.body, self.letter_label):
            widget.bind("<Button-1>", self._handle_focus_request)

        self.color_band.bind("<Button-1>", self._handle_color_click)
        self.color_hint.bind("<Button-1>", self._handle_color_click)
        self.bind("<FocusIn>", self._handle_focus_in)

        self._refresh_styles()

    def get_letter(self) -> str:
        return self.letter

    def set_letter(self, letter: str) -> None:
        self.letter = letter[:1].upper()
        self.letter_label.config(text=self.letter)

    def get_color_state(self) -> str:
        return self.color_state

    def set_color_state(self, color_state: str) -> None:
        if color_state not in self.TILE_BG_BY_COLOR:
            raise ValueError(f"Unknown color state: {color_state!r}")

        self.color_state = color_state
        self._refresh_styles()

    def clear(self) -> None:
        self.letter = ""
        self.color_state = UNSET_COLOR
        self.letter_label.config(text="")
        self._refresh_styles()

    def set_focused(self, is_focused: bool) -> None:
        self.focused = is_focused
        self._refresh_styles()

    def focus_tile(self) -> None:
        self.focus_set()
        self._on_focus(self.index)

    def owns_widget(self, widget: object) -> bool:
        current_widget = widget if isinstance(widget, tk.Misc) else None
        while current_widget is not None:
            if current_widget is self:
                return True
            current_widget = current_widget.master

        return False

    def _handle_focus_request(self, _event: tk.Event) -> str:
        self.focus_tile()
        return "break"

    def _handle_color_click(self, _event: tk.Event) -> str:
        self.focus_tile()
        self._on_color_click(self.index)
        return "break"

    def _handle_focus_in(self, _event: tk.Event) -> None:
        self._on_focus(self.index)

    def _refresh_styles(self) -> None:
        if self.color_state == UNSET_COLOR:
            tile_bg = self.FOCUS_BG if self.focused else self.DEFAULT_BG
            band_bg = self.UNSET_BAND_BG
            hint_fg = "#5b5447"
        else:
            tile_bg = self.TILE_BG_BY_COLOR[self.color_state]
            band_bg = tile_bg
            hint_fg = "#f8f9fb"

        border_color = self.FOCUS_BORDER if self.focused else self.DEFAULT_BORDER
        text_fg = self.TEXT_FG_BY_COLOR[self.color_state]

        self.config(
            bg=tile_bg,
            highlightbackground=border_color,
            highlightcolor=border_color,
        )
        self.body.config(bg=tile_bg)
        self.letter_label.config(bg=tile_bg, fg=text_fg)
        self.color_band.config(bg=band_bg)
        self.color_hint.config(bg=band_bg, fg=hint_fg)
