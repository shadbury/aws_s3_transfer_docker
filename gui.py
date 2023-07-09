import tkinter as tk
from tkinter import ttk
import logging
from terminal import Terminal
from profile_selection import ProfileSelection
from transfer_options import TransferOptions





class S3TransferApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("S3 Transfer App")

        self.profile_selection = ProfileSelection(self)
        self.transfer_options = TransferOptions(self)
        self.terminal = Terminal(self)

        self.profile_selection.grid(row=0, column=0, sticky="nsew")
        self.transfer_options.grid(row=1, column=0, sticky="nsew")
        self.terminal.grid(row=2, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=5)
        self.grid_columnconfigure(0, weight=1)

        self.protocol("WM_DELETE_WINDOW", self._exit_app)

        # Set up logging to redirect logs to the terminal widget
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.handler = TextWidgetHandler(self.terminal)
        self.logger.addHandler(self.handler)

    def _exit_app(self):
        self.destroy()

    def run(self):
        self.mainloop()


class TextWidgetHandler(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        message = self.format(record)
        self.widget.write_output(message)


if __name__ == "__main__":
    app = S3TransferApp()
    app.run()
