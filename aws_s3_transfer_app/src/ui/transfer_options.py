import tkinter as tk
from tkinter import ttk
from aws import get_buckets, transfer_files
from ui.autocomplete import AutocompleteCombobox

class TransferOptions(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master

        self.source_bucket_label = ttk.Label(self, text="Source Bucket:")
        self.source_bucket_label.grid(row=0, column=0, sticky="w")

        self.source_bucket_entry = AutocompleteCombobox(self)
        self.source_bucket_entry.grid(row=0, column=1, sticky="we")

        self.destination_bucket_label = ttk.Label(self, text="Destination Bucket:")
        self.destination_bucket_label.grid(row=1, column=0, sticky="w")

        self.destination_bucket_entry = AutocompleteCombobox(self)
        self.destination_bucket_entry.grid(row=1, column=1, sticky="we")

        self.source_profile = None
        self.destination_profile = None

    def update_buckets(self, source_profile):
        self.source_profile = source_profile
        buckets = get_buckets(source_profile)
        self.source_bucket_entry.set_completion_list(buckets)

    def transfer(self):
        source_bucket = self.source_bucket_entry.get()
        destination_bucket = self.destination_bucket_entry.get()
        encrypt_source = self.encrypt_source_var.get()
        encrypt_destination = self.encrypt_destination_var.get()
        encryption_algorithm = self.encryption_algorithm_entry.get()

        transfer_files(
            self.source_profile,
            self.destination_profile,
            source_bucket,
            destination_bucket,
            encrypt_source,
            encrypt_destination,
            encryption_algorithm
        )
