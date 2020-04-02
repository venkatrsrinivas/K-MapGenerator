import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter.filedialog import askopenfilename as askopenfilename
import sys
import backend
from tkinter import *
from functools import partial
from traceback import format_exc

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
helpmenu.add_command(label="Credits", command=credits)

canvas = Canvas(root, width=800, height=600, bd=0, highlightthickness=0)
canvas.pack()

currentKMap, variables, original = backend.main()
canvas.create_text(400, 15, text="Expression: " + str(original), font=('Arial', 18))
    
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

groupingsmap = {}

grouping_text_id = None

def redrawKmap():
    grouping_list = "Groupings:\n"
    w.tag_add("all", "1.0", str(currentKMap.rows)+"."+str(currentKMap.columns-1))
    w.tag_config("all", background="white", foreground="black")
    groupings = currentKMap.getGroupings()
    colors = ['Red', 'Pink', 'Orange', 'Yellow', 'Light Green', 'Dark Green', 'Blue', 'Purple']
    color = 0
    groupingsmap.clear()
    for grouping in groupings:
        grouping_list = grouping_list + str(grouping) + "\n"
        groupingsmap[colors[color]] = grouping
        thisgrouping = []
        if str(grouping[0][0])[0] == '(':
            print("Nested grouping")
            # Nested, this grouping is actually two merged groupings
            thisgrouping.append(grouping[0])
            thisgrouping.append(grouping[1])
        else:
            print("Non-nested grouping")
            # This is just one normal rectangular grouping
            thisgrouping.append(grouping)
        for rectangle in thisgrouping:
            y1 = str(rectangle[0][0]+1)
            x1 = str(rectangle[0][1]*2)
            y2 = str(rectangle[1][0]+1)
            x2 = str(rectangle[1][1]*2+1)
            print("x1:"+x1)
            print("y1:"+y1)
            print("x2:"+x2)
            print("y2:"+y2)
            if y2 < y1:
                for y in range(int(y1), int(currentKMap.columns*2+1)):
                    w.tag_add(str(str(y)+'.'+x1+'.'+str(y)+'.'+x2), str(str(y)+'.'+x1),str(str(y)+'.'+x2))
                    w.tag_config(str(str(y)+'.'+x1+'.'+str(y)+'.'+x2), background=colors[color], foreground="white")
                for y in range(0, int(int(y2)+1)):
                    w.tag_add(str(str(y)+'.'+x1+'.'+str(y)+'.'+x2), str(str(y)+'.'+x1),str(str(y)+'.'+x2))
                    w.tag_config(str(str(y)+'.'+x1+'.'+str(y)+'.'+x2), background=colors[color], foreground="white")
            else:
                for y in range(int(y1), int(y2)+1):
                    if x2 < x1:
                        # Highlight from x1 to the end
                        w.tag_add(str(str(y)+'.'+x1+'.'+str(y)+'.'+ str(currentKMap.columns*2)), str(str(y)+'.'+x1),str(str(y)+'.'+str(currentKMap.columns*2)))
                        w.tag_config(str(str(y)+'.'+x1+'.'+str(y)+'.'+ str(currentKMap.columns*2)), background=colors[color], foreground="white")
                        # Highlight from 0 to x2
                        w.tag_add(str(str(y)+'.'+ str(0) +'.'+str(y)+'.'+ x2), str(str(y)+'.'+str(0)),str(str(y)+'.'+x2))
                        w.tag_config(str(str(y)+'.'+str(0)+'.'+str(y)+'.'+ x2), background=colors[color], foreground="white")
                    else:
                        w.tag_add(str(str(y)+'.'+x1+'.'+str(y)+'.'+x2), str(str(y)+'.'+x1),str(str(y)+'.'+x2))
                        w.tag_config(str(str(y)+'.'+x1+'.'+str(y)+'.'+x2), background=colors[color], foreground="white")
        color = color + 1
    canvas.itemconfig(grouping_text_id, text=grouping_list)

def createGrouping(x1, y1, x2, y2):
    try:
        result = currentKMap.addGrouping((int(y1.get()),int(x1.get())),(int(y2.get()),int(x2.get())))
    except Exception as e:
        messagebox.showerror("Error", "Error: " + str(e) + "\n\nMore details for developers: " + str(format_exc()))
        return
    redrawKmap()

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
    canvas.create_line(250, 80, 310, 140)
    canvas.create_text(290, 95, text=variables[0]+variables[1], font=('Arial bold', 20))
    canvas.create_text(270, 125, text=variables[2], font=('Arial bold', 20))
    canvas.create_text(325, 120, text="00", font=('Arial', 20))
    canvas.create_text(360, 120, text="01", font=('Arial', 20))

    canvas.create_text(395, 120, text="11", font=('Arial', 20))
    canvas.create_text(430, 120, text="10", font=('Arial', 20))

    canvas.create_text(300, 165, text="0", font=('Arial', 20))
    canvas.create_text(300, 215, text="1", font=('Arial', 20))
elif numVars == 4:
    print("4 variables")
    canvas.create_line(250, 80, 310, 140)
    canvas.create_text(290, 95, text=variables[0]+variables[1], font=('Arial bold', 20))
    canvas.create_text(265, 125, text=variables[2]+variables[3], font=('Arial bold', 20))
    canvas.create_text(325, 120, text="00", font=('Arial', 20))
    canvas.create_text(360, 120, text="01", font=('Arial', 20))

    canvas.create_text(395, 120, text="11", font=('Arial', 20))
    canvas.create_text(430, 120, text="10", font=('Arial', 20))

    canvas.create_text(300, 165, text="00", font=('Arial', 20), angle=90)
    canvas.create_text(300, 215, text="01", font=('Arial', 20), angle=90)
    canvas.create_text(300, 265, text="11", font=('Arial', 20), angle=90)
    canvas.create_text(300, 315, text="10", font=('Arial', 20), angle=90)
else:
    print("> 4 variables")
    messagebox.showerror("Error", "Error: Expressions with more than 4 variables are not supported at this time. Please choose another file to load.")

canvas.create_text(200, 375, text="  Create Grouping  ", font=('Arial', 20))
canvas.create_text(600, 375, text="  Merge Groupings  ", font=('Arial', 20))
canvas.create_line(80, 400, 330, 400)
canvas.create_line(475, 400, 725, 400)
canvas.create_text(100, 420, text="Upper-Left Coordinates:", font=('Arial', 12))
canvas.create_text(300, 420, text="Lower-Right Coordinates:", font=('Arial', 12))
canvas.create_text(34, 450, text="Y=", font=('Arial', 10))
canvas.create_text(110, 450, text="X=", font=('Arial', 10))
canvas.create_text(230, 450, text="Y=", font=('Arial', 10))
canvas.create_text(310, 450, text="X=", font=('Arial', 10))
create_grouping_ul_y = tk.Entry(canvas, width=6)
create_grouping_ul_x = tk.Entry(canvas, width=6)
create_grouping_lr_y = tk.Entry(canvas, width=6)
create_grouping_lr_x = tk.Entry(canvas, width=6)
create_grouping_ul_y.place(relx=.06, rely=.82, anchor=SW)
create_grouping_ul_x.place(relx=.16, rely=.82, anchor=SW)
create_grouping_lr_y.place(relx=.305, rely=.82, anchor=SW)
create_grouping_lr_x.place(relx=.405, rely=.82, anchor=SW)

submitGrouping = Button(root, text="Create Grouping", command=partial(createGrouping, create_grouping_ul_x, create_grouping_ul_y, create_grouping_lr_x, create_grouping_lr_y))
submitGrouping.place(relx=.19, rely=.81)

canvas.create_text(540, 420, text="Grouping 1:", font=('Arial', 12))
canvas.create_text(540, 450, text="Grouping 2:", font=('Arial', 12))

choices1 = ['Red', 'Pink', 'Orange', 'Yellow', 'Light Green', 'Dark Green', 'Blue', 'Purple']
var1 = tk.StringVar()
var1.set('Select')
popupMenu1 = tk.OptionMenu(canvas, var1, *choices1)
popupMenu1.place(relx=.74, rely=0.72)

choices2 = ['Red', 'Pink', 'Orange', 'Yellow', 'Light Green', 'Dark Green', 'Blue', 'Purple']
var2 = tk.StringVar()
var2.set('Select')
popupMenu2 = tk.OptionMenu(canvas, var2, *choices2)
popupMenu2.place(relx=.74, rely=0.775)


def merge(first, second):
    one = groupingsmap[first.get()]
    two = groupingsmap[second.get()]
    try:
        currentKMap.combineGrouping(one, two, True)
    except Exception as e:
        messagebox.showerror("Error", "Error: " + str(e) + "\n\nMore details for developers: " + str(format_exc()))
        return
    redrawKmap()
    



submitMerge = Button(root, text="Merge Groupings", command=partial(merge, var1, var2))
submitMerge.place(relx=.67, rely=.81)


canvas.create_text(100, 530, text="Final Answer: ", font=('Arial', 20))
answer = Text(canvas, width=36, height=1, font=("Arial", 20))
answer.place(relx=.57, rely=.976, anchor=S)


def check(kmap):
    valid = True
    for x in kmap.groupings:
        for y in kmap.groupings:
            if x is not y and valid:
                try:
                    kmap.combineGrouping(x, y, False)
                except:
                    continue
                finally:
                    valid = False
                    messagebox.showerror("Error", "Two or more adjacent groupings can be merged.")
    if valid:
        print("Passed merge check")
    redrawKmap()

wum = Button(canvas, text='''Check
Answer''', font=('Arial', 11), command=partial(check, currentKMap))
wum.place(relx=.955, rely=.985, anchor=S)


def instructions():
    messagebox.showinfo("Instructions", "Use Create Grouping to create a rectangular grouping. \n\nTo define a grouping, specify the upper-left and lower-right coordinates of the grouping on the K-Map. The upper-left corner is (0, 0). \n\nTo create non-rectangular groupings, create multiple groupings and merge them using Merge Groupings. \n\nOnce all the groupings are constructed, use them to simplify the expression; enter your final answer under Final Answer and click Check Answer to verify if you are correct.\n\nSyntax:\nNOT: ~\nAND: ^\nOR: |\nIF: ->\nIFF: <->.\nAll operators are either unary (not) or binary (and, or, if, iff) and there is no support for a generalized notation. This means that A & B & C will thrown an error, you must do A & (B & C).")

submitMerge = Button(root, text="Instructions", command=instructions)
submitMerge.place(relx=.15, rely=.35, anchor=W)

grouping_text_id = canvas.create_text(630, 200, text="Groupings:", font=('Arial', 12))




#Keep Program Alive
tk.mainloop()
