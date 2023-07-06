import tkinter as tk
from tkinter import messagebox

class Window:
    def __init__(self, master):

        mainframe = tk.Frame(master)
        mainframe.pack()

        mainmenu = tk.Menu(mainframe)
        master.config(menu = mainmenu)

        filemenu = tk.Menu(mainframe)
        filemenu.add_command(label="New File", command = self.func)

        exportmenu = tk.Menu(mainframe)
        exportmenu.add_command(label="New export", command = self.func)
        
        filemenu.add_cascade(label = "export Menu", menu = exportmenu)
        mainmenu.add_cascade(label = "File Menu", menu = filemenu)

        W = tk.Message(master, text="Hello World")  
        W.pack()



    def func(self):
        print("placeholder")
    



root = tk.Tk()
root.geometry('300x200')
window = Window(root)
root.mainloop()