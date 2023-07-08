import tkinter as tk
from tkinter import scrolledtext


class Terminal(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.terminal_text = scrolledtext.ScrolledText(self, state="disabled")
        self.terminal_text.configure(font=("Courier", 10))

        self.terminal_text.pack(expand=True, fill=tk.BOTH)

    def write_output(self, message):
        self.terminal_text.config(state="normal")
        self.terminal_text.insert(tk.END, message + "\n")
        self.terminal_text.config(state="disabled")

    def clear_output(self):
        self.terminal_text.config(state="normal")
        self.terminal_text.delete(1.0, tk.END)
        self.terminal_text.config(state="disabled")
