import tkinter as tk
from profile_selection import ProfileSelection
from transfer_options import TransferOptions
from terminal import Terminal


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

    def update_profiles(self):
        config_path = os.path.expanduser("~/.aws/config")
        credentials_path = os.path.expanduser("~/.aws/credentials")

        profiles = get_config_profiles(config_path) + get_credentials_profiles(credentials_path)
        self.source_profile_entry.set_completion_list(profiles)
        self.destination_profile_entry.set_completion_list(profiles)

    def update_transfer_options(self, event=None):
        self.transfer_options.update_buckets()



    def run(self):
        self.parent.mainloop()
