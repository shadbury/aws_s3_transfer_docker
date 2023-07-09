import tkinter as tk
from tkinter import ttk
from autocomplete import AutocompleteCombobox
from aws import get_profiles

class ProfileSelection(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master

        self.source_profile_label = ttk.Label(self, text="Source Profile:")
        self.source_profile_label.grid(row=0, column=0, sticky="w")

        self.source_profile_entry = AutocompleteCombobox(self)
        self.source_profile_entry.grid(row=0, column=1, sticky="we")

        self.destination_profile_label = ttk.Label(self, text="Destination Profile:")
        self.destination_profile_label.grid(row=1, column=0, sticky="w")

        self.destination_profile_entry = AutocompleteCombobox(self)
        self.destination_profile_entry.grid(row=1, column=1, sticky="we")

        self.update_profiles()

    def update_profiles(self):
        profiles = get_profiles()
        self.source_profile_entry.set_completion_list(profiles)
        self.destination_profile_entry.set_completion_list(profiles)

        # Set the initial values for the dropdowns
        self.source_profile_entry.set('')
        self.destination_profile_entry.set('')
