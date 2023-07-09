import tkinter as tk
from autocomplete import AutocompleteEntry
from aws import get_config_profiles, get_credentials_profiles, get_bucket_list, is_bucket_encrypted



class SourceDestinationProfiles(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        self.source_profile_label = tk.Label(self, text="Source Profile:")
        self.source_profile_entry = AutocompleteEntry(self)
        self.destination_profile_label = tk.Label(self, text="Destination Profile:")
        self.destination_profile_entry = AutocompleteEntry(self)
        
        self.source_profile_label.grid(row=0, column=0, sticky="e")
        self.source_profile_entry.grid(row=0, column=1, padx=5, pady=5)
        self.destination_profile_label.grid(row=1, column=0, sticky="e")
        self.destination_profile_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self._load_profiles()

    def _load_profiles(self):
        profiles = get_config_profiles() + get_credentials_profiles()
        self.source_profile_entry.update_list(profiles)
        self.destination_profile_entry.update_list(profiles)

    def get_source_profile(self):
        return self.source_profile_entry.get()

    def get_destination_profile(self):
        return self.destination_profile_entry.get()

    def get_source_bucket_list(self):
        profile = self.get_source_profile()
        return get_bucket_list(profile)

    def get_destination_bucket_list(self):
        profile = self.get_destination_profile()
        return get_bucket_list(profile)

    def is_source_bucket_encrypted(self, bucket):
        profile = self.get_source_profile()
        return is_bucket_encrypted(profile, bucket)

    def is_destination_bucket_encrypted(self, bucket):
        profile = self.get_destination_profile()
        return is_bucket_encrypted(profile, bucket)
