import tkinter as tk
from tkinter import ttk


class AutocompleteCombobox(ttk.Combobox):
    def __init__(self, master, completevalues=[], **kwargs):
        self.completevalues = completevalues
        self.original_values = completevalues
        self.var = tk.StringVar()
        super().__init__(master, textvariable=self.var, **kwargs)
        self.var.trace("w", self.on_entry_change)
        self.bind("<FocusIn>", self.restore_original_values)
        self.autocomplete_listbox = None  # Initialize autocomplete listbox attribute

    def set_completion_list(self, completevalues):
        self.completevalues = completevalues
        self.original_values = completevalues

    def on_entry_change(self, *args):
        entered_text = self.var.get()
        self.filter_dropdown_values(entered_text)

        if entered_text:
            self.show_autocomplete_text(entered_text)
        else:
            self.hide_autocomplete_text()

    def restore_original_values(self, *args):
        self.configure(values=self.original_values)

    def filter_dropdown_values(self, text):
        matching_values = [
            value for value in self.completevalues if text.lower() in value.lower()
        ]
        self.configure(values=matching_values)

    def show_autocomplete_text(self, entered_text):
        if self.autocomplete_listbox:
            self.autocomplete_listbox.delete(0, tk.END)
        else:
            self.autocomplete_listbox = tk.Listbox(width=self.cget("width"))
            self.autocomplete_listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

        for value in self.completevalues:
            if value.lower().startswith(entered_text.lower()):
                self.autocomplete_listbox.insert(tk.END, value)

        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        self.autocomplete_listbox.place(x=x, y=y)

    def hide_autocomplete_text(self):
        if self.autocomplete_listbox:
            self.autocomplete_listbox.delete(0, tk.END)
            self.autocomplete_listbox.place_forget()

    def on_listbox_select(self, event):
        selected_value = self.autocomplete_listbox.get(self.autocomplete_listbox.curselection())
        self.var.set(selected_value)
        self.hide_autocomplete_text()
        self.icursor(tk.END)
