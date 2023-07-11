import tkinter as tk
from tkinter import ttk


class AutocompleteCombobox(ttk.Combobox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._completion_list = []
        self._hits = []

        self.bind("<KeyRelease>", self.handle_key_release)
        self.bind("<Button-1>", self.handle_button_click)

    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list, key=str.lower)

    def handle_key_release(self, event):
        entered_text = self.get()
        if entered_text:
            self._hits = [hit for hit in self._completion_list if hit.lower().startswith(entered_text.lower())]
            self._hit_index = 0
            self['values'] = self._hits
            self.focus()
        else:
            self._hits = []

    def autocomplete(self):
        if self._hits:
            self.delete(0, tk.END)
            self.insert(tk.END, self._hits[self._hit_index])
            self.icursor(tk.END)

    def handle_button_click(self, event):
        self.autocomplete()
