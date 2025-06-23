import tkinter as tk
from tkinter import StringVar, Entry, OptionMenu, Button, messagebox, Text, Scrollbar, RIGHT, Y
from source_code.utility.constant.color import Color


class View:
    def __init__(self, on_submit_callback=None):
        self.on_submit_callback = on_submit_callback
        self.root = tk.Tk()
        self.root.title("Wordle Guess Input")
        self.root.resizable(False, False)

        self.letter_entries = []
        self.color_vars = []

        self.result_text = None
        self.__build_ui()

    def __build_ui(self):
        grid_frame = tk.Frame(self.root)
        grid_frame.pack(pady=10, padx=10)

        # --- Row 0: Letter Inputs ---
        for i in range(5):
            entry = Entry(grid_frame, width=4, font=("Arial", 24), justify="center")
            entry.grid(row=0, column=i, padx=8, pady=5)
            entry.bind("<KeyRelease>", lambda event, idx=i: self.__on_letter_typed(event, idx))
            self.letter_entries.append(entry)
        
        self.letter_entries[0].focus_set()

        # --- Row 1: Color Dropdowns ---
        for i in range(5):
            var = StringVar()
            var.set("")  # Force explicit selection
            dropdown = OptionMenu(grid_frame, var, *[color.value for color in Color])
            dropdown.config(width=6)  # Narrower width for alignment
            dropdown.grid(row=1, column=i, padx=8, pady=2)
            self.color_vars.append(var)

        # --- Submit Button ---
        submit_btn = Button(
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

        # --- Result Text with Wrapping ---
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
        self.scrollbar.config(command=self.result_text.yview)

    def get_letter_color_inputs(self):
        return [
            (entry.get().strip().lower(), var.get())
            for entry, var in zip(self.letter_entries, self.color_vars)
        ]

    def on_submit(self):
        data = self.get_letter_color_inputs()

        if not all(len(letter) == 1 and letter.isalpha() for letter, _ in data):
            messagebox.showerror("Input Error", "Each letter must be a single alphabetical character.")
            return

        if not all(color for _, color in data):
            messagebox.showerror("Input Error", "You must select a color for each letter.")
            return

        if self.on_submit_callback:
            self.on_submit_callback()

    def show_result(self, text: str):
        self.result_text.config(state="normal")           
        self.result_text.delete("1.0", tk.END)            
        self.result_text.insert(tk.END, f"Results:\n{text}")  
        self.result_text.config(state="disabled")        

    def reset(self):
        for entry in self.letter_entries:
            entry.delete(0, tk.END)
        for var in self.color_vars:
            var.set("")

    def run(self):
        self.root.mainloop()

    def __on_letter_typed(self, event, idx):
        entry = self.letter_entries[idx]
        raw_value = entry.get()

        # Handle backspace: move to previous box if empty
        if event.keysym == "BackSpace":
            if not raw_value and idx > 0:
                prev_entry = self.letter_entries[idx - 1]
                prev_entry.focus_set()
            return

        # Sanitize pasted/typed input: keep only letters, uppercased
        letters = [char.upper() for char in raw_value if char.isalpha()]
        if not letters:
            entry.delete(0, tk.END)
            return

        # Fill current + next boxes with typed/pasted chars
        for offset, char in enumerate(letters):
            target_idx = idx + offset
            if target_idx >= len(self.letter_entries):
                break
            target_entry = self.letter_entries[target_idx]
            target_entry.delete(0, tk.END)
            target_entry.insert(0, char)

        # Focus next box, or last filled one
        final_focus = min(idx + len(letters), len(self.letter_entries)) - 1
        self.letter_entries[final_focus].focus_set()
