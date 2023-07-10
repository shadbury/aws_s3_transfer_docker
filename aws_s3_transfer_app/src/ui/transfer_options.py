import tkinter as tk
from tkinter import ttk
from src.aws import get_profiles  # Import get_profiles directly

class TransferOptions(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Create source and destination profile selection dropdowns
        self.source_profile_label = tk.Label(self, text="Source Profile:")
        self.source_profile_dropdown = CustomDropdown(self)

        self.destination_profile_label = tk.Label(self, text="Destination Profile:")
        self.destination_profile_dropdown = CustomDropdown(self)

        # Place the widgets using grid layout
        self.source_profile_label.grid(row=0, column=0, sticky="e")
        self.source_profile_dropdown.grid(row=0, column=1, padx=10)
        self.destination_profile_label.grid(row=1, column=0, sticky="e")
        self.destination_profile_dropdown.grid(row=1, column=1, padx=10)

        # Update profiles initially
        self.update_profiles()

    def update_profiles(self):
        config_profiles = get_profiles("config")
        credential_profiles = get_profiles("credentials")

        for profile in config_profiles:
            if isinstance(profile, str):
                profile_name = profile.replace('Profile ', '')
            else:
                profile_name = profile.get('name', '').replace('Profile ', '')
            self.source_profile_dropdown.add_option(profile_name, tag="Config")
            self.destination_profile_dropdown.add_option(profile_name, tag="Config")

        for profile in credential_profiles:
            self.source_profile_dropdown.add_option(profile, tag="Cred")
            self.destination_profile_dropdown.add_option(profile, tag="Cred")

class CustomDropdown(ttk.Combobox):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.tag_style = ttk.Style()
        self.tag_style.configure("Config.TCombobox",
                                 background="#EAEAEA",  # Set gray background color
                                 padding=4,  # Add padding to create a bubble appearance
                                 borderwidth=1,
                                 relief="solid",
                                 foreground="blue")
        self.tag_style.configure("Cred.TCombobox",
                                 background="#EAEAEA",
                                 padding=4,
                                 borderwidth=1,
                                 relief="solid",
                                 foreground="green")
        self["style"] = "TCombobox"

    def add_option(self, text, tag):
        self.tag_style.configure(f"{tag}.TCombobox",
                                 background="#EAEAEA",
                                 padding=4,
                                 borderwidth=1,
                                 relief="solid",
                                 foreground="blue" if tag == "Config" else "green")
        self["values"] = tuple(list(self["values"]) + [(text, tag)])
