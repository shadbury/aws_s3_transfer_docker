import tkinter as tk
from tkinter import ttk
from autocomplete import AutocompleteCombobox
from aws import AWS


class ProfileSelection(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.source_profile_label = ttk.Label(self, text="Source Profile:")
        self.source_profile_combobox = AutocompleteCombobox(self, values=[])
        self.destination_profile_label = ttk.Label(self, text="Destination Profile:")
        self.destination_profile_combobox = AutocompleteCombobox(self, values=[])

        self.source_profile_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.source_profile_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.destination_profile_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.destination_profile_combobox.grid(row=1, column=1, padx=5, pady=5)

        self.source_profile_combobox.bind("<<ComboboxSelected>>", self.source_profile_selected)
        self.destination_profile_combobox.bind("<<ComboboxSelected>>", self.destination_profile_selected)

    def source_profile_selected(self, event):
        selected_profile = self.source_profile_combobox.get()
        if selected_profile:
            # Logic to handle the selected source profile
            print(f"Selected source profile: {selected_profile}")

    def destination_profile_selected(self, event):
        selected_profile = self.destination_profile_combobox.get()
        if selected_profile:
            # Logic to handle the selected destination profile
            print(f"Selected destination profile: {selected_profile}")

    def update_profiles(self):
        aws = AWS()
        config_profiles = aws.get_config_profiles()
        credential_profiles = aws.get_credentials_profiles()
        profiles = config_profiles + credential_profiles
        self.source_profile_combobox["values"] = profiles
        self.destination_profile_combobox["values"] = profiles

    def hide_profiles(self):
        self.source_profile_label.grid_remove()
        self.source_profile_combobox.grid_remove()
        self.destination_profile_label.grid_remove()
        self.destination_profile_combobox.grid_remove()

    def show_profiles(self):
        self.source_profile_label.grid()
        self.source_profile_combobox.grid()
        self.destination_profile_label.grid()
        self.destination_profile_combobox.grid()
