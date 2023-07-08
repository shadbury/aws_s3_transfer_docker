from gui import S3TransferApp

if __name__ == "__main__":
    app = S3TransferApp()
    app.profile_selection.update_profiles()  # Call the update_profiles method to populate the drop-downs
    app.mainloop()
