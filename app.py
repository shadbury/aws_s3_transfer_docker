import tkinter as tk
from s3_transfer_app import S3TransferApp

if __name__ == "__main__":
    root = tk.Tk()
    app = S3TransferApp(root)
    app.pack()
    root.mainloop()
