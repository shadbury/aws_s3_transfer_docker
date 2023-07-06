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
T = tk.Text(root, bg="White", fg="grey")
l = tk.Label(root, text="go fuck yourself")
l.config(font =("Courier", 14))
 
Fact = """A man can be arrested in
Italy for wearing a skirt in public."""
 
# Create button for next text.
b1 = tk.Button(root, text = "Next", )
 
# Create an Exit button.
b2 = tk.Button(root, text = "Exit",
            command = root.destroy)
 
l.pack()
T.pack()
b1.pack()
b2.pack()
 
# Insert The Fact.
T.insert(tk.END, Fact)
T.pack()
root.mainloop()