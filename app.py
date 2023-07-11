import tkinter as tk
from src.ui.profile_selection import ProfileSelection
from src.ui.transfer_options import TransferOptions
from src.ui.terminal import Terminal
from src.logging_manager import configure_logging

class S3TransferApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.terminal = Terminal(self)
        self.profile_selection = ProfileSelection(self, self.terminal)
        self.transfer_options = TransferOptions(self)

        self.transfer_options.pack(side="top", fill="x")
        self.terminal.pack(side="top", fill="both", expand=True)

        self.transfer_options.bind("<<ProfilesUpdated>>", self.update_transfer_options)

        # Configure logging
        configure_logging(self.terminal)

    def update_transfer_options(self, event=None):
        source_profile, destination_profile = self.profile_selection.get_selected_profiles()

        # Clear the source and destination options
        self.transfer_options.clear_source_options()
        self.transfer_options.clear_destination_options()

        # Retrieve profiles and update the transfer options
        profiles = get_profiles()
        self.transfer_options.update_profiles(profiles)

        # Set the selected profiles in the transfer options
        if source_profile:
            self.transfer_options.set_source_profile(source_profile)
        if destination_profile:
            self.transfer_options.set_destination_profile(destination_profile)


if __name__ == "__main__":
    root = tk.Tk()
    app = S3TransferApp(root)
    app.pack()
    root.mainloop()
