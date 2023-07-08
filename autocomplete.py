import tkinter as tk
from tkinter import ttk


class AutocompleteCombobox(ttk.Combobox):
    def __init__(self, parent, values, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.values = values
        self.var = self["textvariable"]
        if not self.var:
            self.var = self["textvariable"] = tk.StringVar()
        self.var.trace("w", self.update_values)
        self.bind("<KeyRelease>", self.on_key_release)

    def update_values(self, *args):
        entered_text = self.var.get()
        if entered_text:
            matching_values = [value for value in self.values if value.startswith(entered_text)]
        else:
            matching_values = self.values
        self["values"] = matching_values

    def on_key_release(self, event):
        if event.keysym == "BackSpace":
            self.update_values()
