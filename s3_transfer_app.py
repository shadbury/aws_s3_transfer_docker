import tkinter as tk
from tkinter import ttk
from profile_selection import ProfileSelection
from transfer_options import TransferOptions
from terminal import Terminal
from s3_operations import copy_object, delete_object, encrypt_object


class S3TransferApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("S3 Transfer App")

        self.profile_selection = ProfileSelection(self)
        self.transfer_options = TransferOptions(self)
        self.terminal = Terminal(self)

        self.profile_selection.grid(row=0, column=0, sticky="nsew")
        self.transfer_options.grid(row=1, column=0, sticky="nsew")
        self.terminal.grid(row=2, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=5)
        self.grid_columnconfigure(0, weight=1)

        self.protocol("WM_DELETE_WINDOW", self._exit_app)

    def _exit_app(self):
        self.destroy()

    def run(self):
        self.mainloop()

    def copy_object(self):
        """
        Copy the object from the source bucket to the destination bucket.
        """
        source_profile = self.profile_selection.get_source_profile()
        destination_profile = self.profile_selection.get_destination_profile()
        source_bucket = self.transfer_options.get_source_bucket()
        destination_bucket = self.transfer_options.get_destination_bucket()
        source_key = self.transfer_options.get_source_key()

        copy_object(source_profile, source_bucket, source_key, destination_profile, destination_bucket)
        self.terminal.write_output(f"Object '{source_key}' copied from '{source_bucket}' to '{destination_bucket}'.")

    def delete_object(self):
        """
        Delete the object from the specified bucket.
        """
        profile = self.profile_selection.get_source_profile()
        bucket = self.transfer_options.get_source_bucket()
        key = self.transfer_options.get_source_key()

        delete_object(profile, bucket, key)
        self.terminal.write_output(f"Object '{key}' deleted from '{bucket}'.")

    def encrypt_object(self):
        """
        Encrypt the object in the specified bucket with the selected algorithm.
        """
        profile = self.profile_selection.get_source_profile()
        bucket = self.transfer_options.get_source_bucket()
        key = self.transfer_options.get_source_key()
        algorithm = self.transfer_options.get_encryption_algorithm()

        encrypt_object(profile, bucket, key, algorithm)
        self.terminal.write_output(f"Object '{key}' in bucket '{bucket}' encrypted with '{algorithm}'.")


if __name__ == "__main__":
    app = S3TransferApp()
    app.run()
