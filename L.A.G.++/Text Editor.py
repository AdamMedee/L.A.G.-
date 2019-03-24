
from tkinter import *

import tkinter.filedialog

import tkinter.messagebox

from tkinter.colorchooser import askcolor

import datetime

import webbrowser

from tkinter.filedialog import askopenfilename, asksaveasfilename

from language import *

from queue import *


InputQ = Queue()


def line():

    lin = "_" * 60

    text.insert(INSERT ,lin)



def date():

    data = datetime.date.today()

    text.insert(INSERT ,data)



def normal():

    text.config(font = ("Courier", 10))



def bold():

    text.config(font = ("Courier", 10, "bold"))



def underline():

    text.config(font = ("Courier", 10, "underline"))



def italic():

    text.config(font = ("Courier" ,10 ,"italic"))



def font():

    (triple ,color) = askcolor()

    if color:

        text.config(foreground=color)



def kill():

    root.destroy()



def about():

    pass



def opn():

    text.delete(1.0 , END)

    file = open(askopenfilename() , 'r')

    if file != '':

        txt = file.read()

        text.insert(INSERT ,txt)

    else:

        pass



def save():

    filename = asksaveasfilename()

    if filename:

        alltext = text.get(1.0, END)

        open(filename, 'w').write(alltext)



def copy():

    text.clipboard_clear()

    text.clipboard_append(text.selection_get())



def paste():

    try:

        teext = text.selection_get(selection='CLIPBOARD')

        text.insert(INSERT, teext)

    except:

        tkMessageBox.showerror("Error" ,"Something went wrong!")



def clear():
    try:

        sel = text.get(SEL_FIRST, SEL_LAST)

        text.delete(SEL_FIRST, SEL_LAST)
    except:
        pass


def clearall():

    text.delete(1.0 , END)



def background():

    (triple ,color) = askcolor()

    if color:

        text.config(background=color)



def about():

    ab = Toplevel(root)

    txt = "Enrix's pad\nRealizzato da Enrix (C)\n http://www.enrixweb.altervista.org\nIl programma è rilasciato sotto licensa GPL"

    la = Label(ab ,text=txt ,foreground='blue')

    la.pack()
# def showloop():
#
# def showvar():
#
def showdoc():

    webbrowser.open("https://docs.google.com/document/d/e/2PACX-1vTcpvXQOE_pVjB85cgMPVd093jPtsxj0-77QnNiQi4S3_8hzpffIX4ZEquO-n5ITNWqyFzu9kZxFysT/pub")



def web():

    webbrowser.open('http://www.enrixweb.altervista.org')

def select_all(event):
    text.tag_add(SEL ,"1.0" ,END)
    text.mark_set(INSERT ,"1.0")
    text.see(INSERT)
    return "break"


def getcurrentline(event):
    global currentInput
    pos=console.index(INSERT).split(".")
    line=console.get(pos[0]+".0",pos[0]+"."+pos[1])
    print(line)
    InputQ.put(line);





def runFile(event):
    runfile()

def runfile():
    global lines,text,console, maxrow
    master = Tk()
    master.geometry("1200x700")
    master.title("Running")
    console = Text(master, height=90, width=90, font=("Courier", 10))

    autoscroll = Scrollbar(master,command=console.yview)
    autoscroll.config(command=console.yview)

    console.pack()
    autoscroll.pack()

    console.tag_config('welcome', foreground="blue")
    console.insert(END, "Hello from the LAG++ development team!\n", 'welcome')

    console.bind("<Return>",getcurrentline)
    #Reserving the rest for Adam for actual compilation of file
    lines=text.get("1.0",END).splitlines()
    code = Code(lines)
    code.run()

    if code.sent:
        console.insert(code.m+"\n",END, 'welcome')
        code.sent = False



root = Tk()

root.geometry("1200x700")

root.title("Lag++ Editor")

menu = Menu(root)



lines=list()
filemenu = Menu(root)

root.config(menu = menu)

menu.add_cascade(label="File", menu=filemenu)

filemenu.add_command(label="Open...", command=opn)

filemenu.add_command(label="Save...", command=save)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=kill)



modmenu = Menu(root)

menu.add_cascade(label="Edit" ,menu = modmenu)

modmenu.add_command(label="Copy", command = copy)

modmenu.add_command(label="Paste", command=paste)

modmenu.add_separator()

modmenu.add_command(label = "Clear", command = clear)

modmenu.add_command(label = "Clear All", command = clearall)







insmenu = Menu(root)

menu.add_cascade(label="Insert" ,menu= insmenu)

insmenu.add_command(label="Date" ,command=date)

insmenu.add_command(label="Line" ,command=line)









formatmenu = Menu(menu)

menu.add_cascade(label="Format" ,menu = formatmenu)

formatmenu.add_cascade(label="Colour...", command = font)

formatmenu.add_separator()

formatmenu.add_radiobutton(label='Normal' ,command=normal)

formatmenu.add_radiobutton(label='Bold' ,command=bold)

formatmenu.add_radiobutton(label='Underline' ,command=underline)

formatmenu.add_radiobutton(label='Italic' ,command=italic)



persomenu = Menu(root)

menu.add_cascade(label="Personalize" ,menu=persomenu)

persomenu.add_command(label="Background...", command=background)


runmenu=Menu(menu)

menu.add_cascade(label="Run",menu=runmenu)

runmenu.add_command(label="Run Module...F5",command=runfile)



helpmenu = Menu(menu)

menu.add_cascade(label="?", menu=helpmenu)

helpmenu.add_command(label="Documentation", command=showdoc)


text = Text(root, height=90, width=90, font = ("Courier", 10))


scroll = Scrollbar(root, command=text.yview)

scroll.config(command=text.yview)

text.config(yscrollcommand=scroll.set)

text.pack(anchor=NW,fill=X)
scroll.pack(side=RIGHT, fill=Y)



text.bind("<Control-Key-a>" ,select_all)
text.bind("<Control-Key-A>" ,select_all)
text.bind("<F5>",runFile)


root.resizable(0 ,0)

root.mainloop()