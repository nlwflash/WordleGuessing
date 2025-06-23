import tkinter as tk
from tkinter import StringVar, Entry, OptionMenu, Button, messagebox, Text, Scrollbar, RIGHT, Y
from tkinter import Frame, Event
from typing import Callable, Optional, List, Tuple
from source_code.utility.constant.color import Color


class View:
    def __init__(self, on_submit_callback: Optional[Callable[[], None]] = None):
        self.on_submit_callback = on_submit_callback
        self.root: tk.Tk = tk.Tk()
        self.root.title("Wordle Guess Input")
        self.root.resizable(False, False)

        self.letter_entries: List[Entry] = []
        self.color_vars: List[StringVar] = []

        self.result_text: Optional[Text] = None
        self.scrollbar: Optional[Scrollbar] = None
        self.result_frame: Optional[Frame] = None

        self.__build_ui()

    def __build_ui(self) -> None:
        grid_frame: Frame = tk.Frame(self.root)
        grid_frame.pack(pady=10, padx=10)

        # --- Row 0: Letter Inputs ---
        for i in range(5):
            entry: Entry = Entry(grid_frame, width=4, font=("Arial", 24), justify="center")
            entry.grid(row=0, column=i, padx=8, pady=5)
            entry.bind("<KeyRelease>", lambda event, idx=i: self.__on_letter_typed(event, idx))
            self.letter_entries.append(entry)

        self.letter_entries[0].focus_set()

        # --- Row 1: Color Dropdowns ---
        for i in range(5):
            var: StringVar = StringVar()
            var.set("")  # Force explicit selection
            dropdown: OptionMenu = OptionMenu(grid_frame, var, *[color.value for color in Color])
            dropdown.config(width=6)
            dropdown.grid(row=1, column=i, padx=8, pady=2)
            self.color_vars.append(var)

        # --- Submit Button ---
        submit_btn: Button = Button(
            self.root,
            text="Submit",
            command=self.on_submit,
            font=("Arial", 14, "bold"),
            width=12,
            height=2
        )
        submit_btn.bind("<Enter>", lambda e: submit_btn.config(bg="lightblue"))
        submit_btn.bind("<Leave>", lambda e: submit_btn.config(bg="SystemButtonFace"))
        submit_btn.pack(pady=(10, 5))

        # --- Result Text with Wrapping + Scroll ---
        self.result_frame = tk.Frame(self.root)
        self.result_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.scrollbar = Scrollbar(self.result_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.result_text = Text(
            self.result_frame,
            wrap="word",
            height=8,
            font=("Arial", 12),
            yscrollcommand=self.scrollbar.set
        )
        self.result_text.pack(fill="both", expand=True)
        self.scrollbar.config(command=self.result_text.yview) # type: ignore

    def get_letter_color_inputs(self) -> List[Tuple[str, str]]:
        return [
            (entry.get().strip().lower(), var.get())
            for entry, var in zip(self.letter_entries, self.color_vars)
        ]

    def on_submit(self) -> None:
        data: List[Tuple[str, str]] = self.get_letter_color_inputs()

        if not all(len(letter) == 1 and letter.isalpha() for letter, _ in data):
            messagebox.showerror("Input Error", "Each letter must be a single alphabetical character.") # type: ignore
            return

        if not all(color for _, color in data):
            messagebox.showerror("Input Error", "You must select a color for each letter.") # type: ignore
            return

        if self.on_submit_callback:
            self.on_submit_callback()

    def show_result(self, text: str) -> None:
        if self.result_text:
            self.result_text.config(state="normal")
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Results:\n{text}")
            self.result_text.config(state="disabled")

    def reset(self) -> None:
        for entry in self.letter_entries:
            entry.delete(0, tk.END)
        for var in self.color_vars:
            var.set("")

    def run(self) -> None:
        self.root.mainloop()

    def __on_letter_typed(self, event: Event, idx: int) -> None:
        entry: Entry = self.letter_entries[idx]
        raw_value: str = entry.get()

        # Handle backspace
        if event.keysym == "BackSpace":
            if not raw_value and idx > 0:
                prev_entry: Entry = self.letter_entries[idx - 1]
                prev_entry.focus_set()
            return

        letters: List[str] = [char.upper() for char in raw_value if char.isalpha()]
        if not letters:
            entry.delete(0, tk.END)
            return

        for offset, char in enumerate(letters):
            target_idx: int = idx + offset
            if target_idx >= len(self.letter_entries):
                break
            target_entry: Entry = self.letter_entries[target_idx]
            target_entry.delete(0, tk.END)
            target_entry.insert(0, char)

        final_focus: int = min(idx + len(letters), len(self.letter_entries)) - 1
        self.letter_entries[final_focus].focus_set()
