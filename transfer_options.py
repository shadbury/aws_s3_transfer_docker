import tkinter as tk
from tkinter import ttk


class TransferOptions(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.delete_source_var = tk.BooleanVar(value=False)
        self.delete_source_checkbox = ttk.Checkbutton(
            self, text="Delete Source", variable=self.delete_source_var
        )

        self.encrypt_destination_var = tk.BooleanVar(value=False)
        self.encrypt_destination_checkbox = ttk.Checkbutton(
            self,
            text="Encrypt Destination",
            variable=self.encrypt_destination_var,
            command=self.on_encrypt_destination_checkbox_toggle,
        )

        self.algorithm_var = tk.StringVar()
        self.algorithm_label = ttk.Label(
            self, text="Encryption Algorithm:", state="disabled"
        )
        self.algorithm_combobox = ttk.Combobox(
            self,
            values=["AES256", "KMS"],
            textvariable=self.algorithm_var,
            state="disabled",
        )

        self.delete_source_checkbox.pack(anchor="w")
        self.encrypt_destination_checkbox.pack(anchor="w")
        self.algorithm_label.pack(anchor="w")
        self.algorithm_combobox.pack(anchor="w")

    def on_encrypt_destination_checkbox_toggle(self):
        if self.encrypt_destination_var.get():
            self.algorithm_label.config(state="enabled")
            self.algorithm_combobox.config(state="enabled")
        else:
            self.algorithm_label.config(state="disabled")
            self.algorithm_combobox.config(state="disabled")

    def get_options(self):
        options = {
            "delete_source": self.delete_source_var.get(),
            "encrypt_destination": self.encrypt_destination_var.get(),
            "encryption_algorithm": self.algorithm_var.get() if self.encrypt_destination_var.get() else None,
        }
        return options
