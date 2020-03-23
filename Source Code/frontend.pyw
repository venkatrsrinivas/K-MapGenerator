import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter.filedialog import askopenfilename as askopenfilename
import sys
import backend
from tkinter import *

#Function For Changing Text in Statusbar (Bottom of Program)
#Arguments: x = New Text To Put In Statusbar.
def statusbar(x): 
    statusb.config(text=x)
    statusb.pack(side=tk.BOTTOM, fill=tk.X)
#Temp Placeholder Function
def notImplemented(): 
    tk.messagebox.showerror("Error", "This feature not implemented yet.")
#Credits Dialog Box
def credits():
    tk.messagebox.showinfo("Credits", "Contributors:\nVenkat Srinivas\nAlexandra Hsueh\nTobias Park\n\nhttps://github.com/venkatrsrinivas/K-MapGenerator")
#Open K-Map File In Program
def open(): 
    file = askopenfilename(filetypes=(("K-Map Files", ".kmap"),))
    return file

#Initialize The Window
root = tk.Tk() 
root.update()
root.update_idletasks()
#Set window size as 800x600
w = 800
h = 600
#Code For Centering Window On The Screen
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2) - 32
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

#Set Title of Program
root.title("K-Map Generator") 
#Disabling Ability To Resize Window b/c It Messes Up Things w/ tkinter
root.resizable(0, 0) 
root.resizable(width=False, height=False)
#Setting Title Again?
root.title("K-Map Generator")
#Setting Up Statusbar
statusb = tk.Label(root, text="status bar", bd=1, relief=tk.SUNKEN, anchor=tk.W)
statusbar("Welcome to K-Map Generator.")

#Setup Topbar Menus
menu = tk.Menu(root) 
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

canvas = Canvas(root, width=800, height=600, bd=0, highlightthickness=0)
canvas.pack()

currentKMap, variables = backend.main()
w = Text(canvas, width=2*(currentKMap.columns)-1, height=currentKMap.rows, font=("Arial", 32))
for x in range(0, currentKMap.rows):
    for y in range(0, currentKMap.columns):
        if(y != currentKMap.columns - 1):
            w.insert(END, str(currentKMap.matrix[x][y]) + ' ')
        else:
            w.insert(END, str(currentKMap.matrix[x][y]))
    w.insert(END, '\n')
w.insert(END, '\n')

w.config(state=DISABLED)



numVars = len(variables)
w.place(relx=.5, rely=.25, anchor=N)
if numVars == 0:
    print("0 variables")
    messagebox.showerror("Error", "Error: This expression has 0 variables and is not valid. Please choose another file to load.")
elif numVars == 1:
    print("1 variables")
    canvas.create_line(310, 90, 360, 140)
    canvas.create_text(345, 100, text=variables[0], font=('Arial bold', 20))
    canvas.create_text(375, 120, text="0", font=('Arial', 20))
    canvas.create_text(410, 120, text="1", font=('Arial', 20))
elif numVars == 2:
    print("2 variables")
    canvas.create_line(310, 90, 360, 140)
    canvas.create_text(345, 100, text=variables[0], font=('Arial bold', 20))
    canvas.create_text(325, 130, text=variables[1], font=('Arial bold', 20))
    canvas.create_text(375, 120, text="0", font=('Arial', 20))
    canvas.create_text(410, 120, text="1", font=('Arial', 20))
    canvas.create_text(350, 165, text="0", font=('Arial', 20))
    canvas.create_text(350, 215, text="1", font=('Arial', 20))

elif numVars == 3:
    print("3 variables")
elif numVars == 4:
    print("4 variables")
else:
    print("> 4 variables")
    messagebox.showerror("Error", "Error: Expressions with more than 4 variables are not supported at this time. Please choose another file to load.")

#Keep Program Alive
tk.mainloop()
