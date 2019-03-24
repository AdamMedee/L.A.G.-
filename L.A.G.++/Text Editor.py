
from tkinter import *

import tkinter.filedialog

import tkinter.messagebox

from tkinter.colorchooser import askcolor

import datetime

import webbrowser

from tkinter.filedialog import askopenfilename, asksaveasfilename




def line():

    lin = "_" * 60

    text.insert(INSERT ,lin)



def date():

    data = datetime.date.today()

    text.insert(INSERT ,data)



def normal():

    text.config(font = ("Arial", 10))



def bold():

    text.config(font = ("Arial", 10, "bold"))



def underline():

    text.config(font = ("Arial", 10, "underline"))



def italic():

    text.config(font = ("Arial" ,10 ,"italic"))



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




def runfile():
    global lines,text
    master = Tk()
    master.geometry("1200x700")
    master.title("Running")

    console = Text(master,height=90,width=90,font=("Arial",10))

    autoscroll = Scrollbar(master,command=console.yview)
    autoscroll.config(command=console.yview)

    #Reserving the rest for Adam for actual compilation of file
    lines=text.get("1.0",END).splitlines()






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



helpmenu = Menu(menu)

menu.add_cascade(label="?", menu=helpmenu)

helpmenu.add_command(label="Documentation", command=showdoc)
# helpmenu.add_command(label = "Loops", command = showloop)

# helpmenu.add_command(label="Website", command = web)

runmenu=Menu(menu)

menu.add_cascade(label="Run",menu=runmenu)

runmenu.add_command(label="Run Module",command=runfile)


text = Text(root, height=90, width=90, font = ("Arial", 10))

# inbox = Text(root,height=45,width=85,font=("Arial",10))
# # outbox = Text(root,height=45,width=85,font=("Arial",10))
# #
# inbox.pack(anchor=NE)
# # outbox.pack(anchor=SE)

scroll = Scrollbar(root, command=text.yview)

scroll.config(command=text.yview)

text.config(yscrollcommand=scroll.set)

text.pack(anchor=NW,fill=X)
scroll.pack(side=RIGHT, fill=Y)



text.bind("<Control-Key-a>" ,select_all)
text.bind("<Control-Key-A>" ,select_all)


root.resizable(0 ,0)

root.mainloop()