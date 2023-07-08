import tkinter as tk
from tkinter import ttk
from profile_selection import ProfileSelection
from transfer_options import TransferOptions
from terminal import Terminal


class S3TransferApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("S3 Transfer App")

        self.profile_selection = ProfileSelection(self)
        self.transfer_options = TransferOptions(self)
        self.terminal = Terminal(self)

        self.profile_selection.grid(row=0, column=0, padx=10, pady=10)
        self.transfer_options.grid(row=1, column=0, padx=10, pady=10)
        self.terminal.grid(row=2, column=0, padx=10, pady=10)

        self.protocol("WM_DELETE_WINDOW", self._exit_app)

    def _exit_app(self):
        self.destroy()

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = S3TransferApp()
    app.run()
