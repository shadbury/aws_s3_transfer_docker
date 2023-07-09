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

        # Set up logging to redirect logs to the terminal widget
        self.configure_logging()

    def write_output(self, message):
        self.terminal_text.config(state="normal")
        self.terminal_text.insert(tk.END, message + "\n")
        self.terminal_text.see(tk.END)  # Scroll to the end of the text
        self.terminal_text.config(state="disabled")

    def configure_logging(self):
        # Create a logging handler that redirects logs to the terminal widget
        log_handler = TextWidgetHandler(self.terminal_text)

        # Remove existing handlers from the root logger
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Set up logging to use the custom handler
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(log_handler)


class TextWidgetHandler(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        msg = self.format(record)
        self.widget.write_output(msg)
