import tkinter as tk
from tkinter import messagebox
from configparser import ConfigParser
import os
import boto3
from functions import transfer_files, list_buckets
from tkinter import ttk
import threading


class S3OperationsGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("S3 Operations")

        # Create the GUI elements
        self.create_profile_window()

    def create_profile_window(self):
        self.profile_frame = tk.LabelFrame(self, text="Profile")
        self.profile_frame.pack(padx=10, pady=10)

        source_label = tk.Label(self.profile_frame, text="Source Profile:")
        source_label.grid(row=0, column=0, padx=5, pady=5)

        self.source_profile_entry = tk.StringVar()
        self.source_profile_dropdown = tk.OptionMenu(self.profile_frame, self.source_profile_entry, ())
        self.source_profile_dropdown.grid(row=0, column=1, padx=5, pady=5)

        destination_label = tk.Label(self.profile_frame, text="Destination Profile:")
        destination_label.grid(row=1, column=0, padx=5, pady=5)

        self.destination_profile_entry = tk.StringVar()
        self.destination_profile_dropdown = tk.OptionMenu(self.profile_frame, self.destination_profile_entry, ())
        self.destination_profile_dropdown.grid(row=1, column=1, padx=5, pady=5)

        enter_button = tk.Button(self.profile_frame, text="Enter", command=self.check_profiles)
        enter_button.grid(row=2, columnspan=2, padx=5, pady=5)

        self.load_profiles()

    def load_profiles(self):
        config = ConfigParser()
        config.read([os.path.expanduser("~/.aws/config"), os.path.expanduser("~/.aws/credentials")])
        sections = config.sections()
        profiles = []

        for section in sections:
            if section.lower() == "default":
                continue
            if section.startswith("profile "):
                profiles.append(section.replace("profile ", ""))
            elif section != "default":
                profiles.append(section)

        self.source_profile_dropdown['menu'].delete(0, 'end')
        self.destination_profile_dropdown['menu'].delete(0, 'end')
        for profile in profiles:
            self.source_profile_dropdown['menu'].add_command(label=profile, command=lambda p=profile: self.source_profile_entry.set(p))
            self.destination_profile_dropdown['menu'].add_command(label=profile, command=lambda p=profile: self.destination_profile_entry.set(p))

    def check_profiles(self):
        source_profile = self.source_profile_entry.get()
        destination_profile = self.destination_profile_entry.get()
        if not source_profile or not destination_profile:
            messagebox.showerror("Error", "Please enter both source and destination profiles.")
            return

        try:
            source_buckets = self.list_buckets(source_profile)
            destination_buckets = self.list_buckets(destination_profile)

            if not source_buckets:
                messagebox.showerror("Error", "No buckets found in the source profile.")
                return

            if not destination_buckets:
                messagebox.showerror("Error", "No buckets found in the destination profile.")
                return

            self.profile_frame.destroy()
            self.create_bucket_window(source_profile, destination_profile, source_buckets, destination_buckets)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def list_buckets(self, profile):
        session = boto3.Session(profile_name=profile)
        s3_client = session.client('s3')
        response = s3_client.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        return buckets

    def create_bucket_window(self, source_profile, destination_profile, source_buckets, destination_buckets):
        self.bucket_frame = tk.LabelFrame(self, text="Bucket")
        self.bucket_frame.pack(padx=10, pady=10)

        source_bucket_label = tk.Label(self.bucket_frame, text="Source Bucket:")
        source_bucket_label.grid(row=0, column=0, padx=5, pady=5)

        self.source_bucket_entry = tk.StringVar()
        self.source_bucket_dropdown = tk.OptionMenu(self.bucket_frame, self.source_bucket_entry, "")
        self.source_bucket_dropdown.grid(row=0, column=1, padx=5, pady=5)

        destination_bucket_label = tk.Label(self.bucket_frame, text="Destination Bucket:")
        destination_bucket_label.grid(row=1, column=0, padx=5, pady=5)

        self.destination_bucket_entry = tk.StringVar()
        self.destination_bucket_dropdown = tk.OptionMenu(self.bucket_frame, self.destination_bucket_entry, "")
        self.destination_bucket_dropdown.grid(row=1, column=1, padx=5, pady=5)

        delete_toggle = tk.BooleanVar()
        delete_toggle.set(False)
        delete_checkbox = tk.Checkbutton(self.bucket_frame, text="Delete Source Files", variable=delete_toggle)
        delete_checkbox.grid(row=2, columnspan=2, padx=5, pady=5)

        transfer_button = tk.Button(self.bucket_frame, text="Transfer Files", command=lambda: self.transfer_files(delete_toggle.get()))
        transfer_button.grid(row=3, columnspan=2, padx=5, pady=5)

        self.source_profile = source_profile

        self.source_bucket_dropdown['menu'].delete(0, 'end')
        self.destination_bucket_dropdown['menu'].delete(0, 'end')
        for bucket in source_buckets:
            self.source_bucket_dropdown['menu'].add_command(label=bucket, command=lambda b=bucket: self.source_bucket_entry.set(b))
        for bucket in destination_buckets:
            self.destination_bucket_dropdown['menu'].add_command(label=bucket, command=lambda b=bucket: self.destination_bucket_entry.set(b))


    def transfer_files(self, delete_files):
        source_profile = self.source_profile_entry.get()
        destination_profile = self.destination_profile_entry.get()
        source_bucket = self.source_bucket_entry.get()
        destination_bucket = self.destination_bucket_entry.get()

        if not source_bucket or not destination_bucket:
            messagebox.showerror("Error", "Please select both source and destination buckets.")
            return

        progress_window = tk.Toplevel(self)
        progress_window.title("Transfer Progress")

        progress_var = tk.DoubleVar()
        remaining_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(progress_window, mode='determinate', variable=progress_var)
        progress_bar.pack(padx=10, pady=10)

        remaining_label = tk.Label(progress_window, textvariable=remaining_var, font=("Arial", 14))
        remaining_label.pack(padx=10)

        # Create a separate thread to execute the transfer process
        transfer_thread = threading.Thread(target=self.execute_transfer, args=(source_profile, destination_profile, source_bucket, destination_bucket, delete_files, progress_var, remaining_var))
        transfer_thread.start()

    def execute_transfer(self, source_profile, destination_profile, source_bucket, destination_bucket, delete_files, progress_var, remaining_var):
        try:
            transfer_files(source_profile, destination_profile, source_bucket, destination_bucket, delete_files, progress_var, remaining_var)
            messagebox.showinfo("Success", "File transfer completed successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = S3OperationsGUI()
    app.mainloop()