import tkinter as tk
from tkinter import scrolledtext
import logging


class Terminal(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.terminal_text = scrolledtext.ScrolledText(self, state="disabled")
        self.terminal_text.configure(font=("Courier", 10))

        self.terminal_text.pack(expand=True, fill=tk.BOTH)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def write_output(self, message):
        self.terminal_text.config(state="normal")
        self.terminal_text.insert(tk.END, message + "\n")
        self.terminal_text.see(tk.END)  # Scroll to the end of the text
        self.terminal_text.config(state="disabled")

        self.logger.info(message)
