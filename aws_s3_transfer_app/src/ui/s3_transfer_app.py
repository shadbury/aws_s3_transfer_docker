import tkinter as tk
from ui.profile_selection import ProfileSelection
from ui.transfer_options import TransferOptions
from ui.terminal import Terminal, TextWidgetHandler
import logging

class S3TransferApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.profile_selection = ProfileSelection(self)
        self.transfer_options = TransferOptions(self)
        self.terminal = Terminal(self)

        self.profile_selection.pack(side="top", fill="x")
        self.transfer_options.pack(side="top", fill="x")
        self.terminal.pack(side="top", fill="both", expand=True)

        self.profile_selection.bind("<<ProfileSelectionChanged>>", self.update_transfer_options)

        self.configure_logging()

    def configure_logging(self):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(TextWidgetHandler(self.terminal))

    def update_transfer_options(self, event=None):
        source_profile = self.profile_selection.source_profile_entry.get()
        self.transfer_options.update_buckets(source_profile)


if __name__ == "__main__":
    root = tk.Tk()
    app = S3TransferApp(root)
    app.pack()
    root.mainloop()
