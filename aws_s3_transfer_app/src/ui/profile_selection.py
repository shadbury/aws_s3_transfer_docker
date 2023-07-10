import tkinter as tk
from tkinter import ttk
from src.aws import get_profiles
from src.access import check_profile_access
from src.logging_manager import configure_logging

class ProfileSelection(tk.Frame):
    def __init__(self, parent, terminal):
        super().__init__(parent)
        self.parent = parent
        self.terminal = terminal

        self.logger = configure_logging(self.terminal)

        self.source_profile_label = ttk.Label(self, text="Source Profile:")
        self.source_profile_entry = ttk.Combobox(self, state="readonly")
        self.destination_profile_label = ttk.Label(self, text="Destination Profile:")
        self.destination_profile_entry = ttk.Combobox(self, state="readonly")

        self.source_profile_label.grid(row=0, column=0, sticky="w")
        self.source_profile_entry.grid(row=0, column=1, sticky="we")
        self.destination_profile_label.grid(row=1, column=0, sticky="w")
        self.destination_profile_entry.grid(row=1, column=1, sticky="we")

        self.bind_events()

        self.update_profiles()  # Update profiles initially

    def update_profiles(self):
        profiles = get_profiles()
        self.source_profile_entry["values"] = profiles
        self.destination_profile_entry["values"] = profiles

    def clear_source_options(self):
        self.source_profile_entry["values"] = []

    def clear_destination_options(self):
        self.destination_profile_entry["values"] = []

    def get_selected_profiles(self):
        source_profile = self.source_profile_entry.get()
        destination_profile = self.destination_profile_entry.get()
        return source_profile, destination_profile

    def set_source_profile(self, profile):
        self.source_profile_entry.set(profile)

    def set_destination_profile(self, profile):
        self.destination_profile_entry.set(profile)

    def bind_events(self):
        self.source_profile_entry.bind("<<ComboboxSelected>>", self.master.update_transfer_options)
        self.destination_profile_entry.bind("<<ComboboxSelected>>", self.master.update_transfer_options)

    def write_output(self, message):
        self.terminal.write_output(message)
