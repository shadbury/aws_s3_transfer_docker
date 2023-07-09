import tkinter as tk
from tkinter import ttk

class AutocompleteCombobox(ttk.Combobox):
    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list, key=str.lower)  # Alphabetically sorted list
        self._hits = []
        self._hit_index = 0
        self._set_completion()

    def _set_completion(self):
        self.delete(0, tk.END)
        if self._hits:
            self.insert(tk.END, self._hits[self._hit_index])
            self.select_range(tk.END, tk.END)

    def _autocomplete(self, delta=0):
        if delta:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
        else:
            entered_text = self.get()
            self._hits = [hit for hit in self._completion_list if hit.lower().startswith(entered_text.lower())]
            self._hit_index = 0

        self._set_completion()

    def on_key_press(self, event):
        if event.keysym == "BackSpace":
            self.delete(tk.ACTIVE + "-1c")
            self._autocomplete()
        elif event.keysym == "Return":
            self._hit_index = 0
            self.event_generate("<<ComboboxSelected>>")
        elif event.keysym == "Down":
            self._autocomplete(1)
        elif event.keysym == "Up":
            self._autocomplete(-1)
        else:
            self._autocomplete()

    def on_focus_in(self, event):
        self._set_completion()


class AutocompleteEntry(tk.Entry):
    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list, key=str.lower)  # Alphabetically sorted list
        self._hits = []
        self._hit_index = 0
        self._original_values = self._completion_list.copy()
        self._restore_original_values()

    def _restore_original_values(self):
        self.delete(0, tk.END)
        self.configure(values=self._original_values)

    def on_key_press(self, event):
        entered_text = self.get()
        self._hits = [hit for hit in self._completion_list if hit.lower().startswith(entered_text.lower())]
        self._hit_index = 0

        if len(self._hits) > 0:
            self.configure(values=self._hits)
        else:
            self._restore_original_values()
