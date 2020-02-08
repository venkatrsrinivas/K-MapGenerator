import tkinter as tk
import tkinter.messagebox
from tkinter.filedialog import askopenfilename as askopenfilename

# function for changing text in the statusbar at bottom of program
# args: x is the new text to put in the statusbar
def statusbar(x): 
    statusb.config(text=x)
    statusb.pack(side=tk.BOTTOM, fill=tk.X)

def notImplemented(): # temporary placeholder function
    tk.messagebox.showerror("Error", "This feature not implemented yet.")

def credits(): # credits dialog box
    tk.messagebox.showinfo("Credits", "Contributors:\nVenkat Srinivas\nAlexandra Hsueh\nTobias Park\n\nhttps://github.com/venkatrsrinivas/K-MapGenerator")

def open(): # opening a K-Map file in the program
    file = askopenfilename(filetypes=(("K-Map Files", ".kmap"),))
    return file

root = tk.Tk() # initialize the window

root.update()
root.update_idletasks()
w = 800 # set window size as 800x600
h = 600

# code for centering window on the screen
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2) - 32
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

root.title("K-Map Generator") # set title of program
root.resizable(0, 0) # disabling ability to resize the window (because that messes things up with tkinter)
root.resizable(width=False, height=False)
root.title("K-Map Generator") # setting title again

statusb = tk.Label(root, text="status bar", bd=1, relief=tk.SUNKEN, anchor=tk.W) # setting up statusbar
statusbar("Welcome to K-Map Generator!")

menu = tk.Menu(root) # setting up topbar menus
root.config(menu=menu)
filemenu = tk.Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=notImplemented)
filemenu.add_command(label="Open", command=open)
filemenu.add_command(label="Save", command=notImplemented)
helpmenu = tk.Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="Instructions", command=notImplemented)
helpmenu.add_command(label="Credits", command=credits)
tk.mainloop() # keep program alive

# initialize canvas where frontend elements live
canvas = tk.Canvas(root, width=800, height=600, bd=0, highlightthickness=0) 
canvas.pack()