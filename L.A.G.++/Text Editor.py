
from tkinter import *

import tkinter.filedialog

import tkinter.messagebox

from tkinter.colorchooser import askcolor

import datetime

import webbrowser

from tkinter.filedialog import askopenfilename, asksaveasfilename


DocString="""
Types


LAG++ supports four types: numbers, strings, booleans, and lists.

Numbers take the form of any rational numbers with an absolute value below 10300 (e.g. 2, 4.2, -6.9, 128, -4, 6.23242, 0). Note that if a user attempts to use any number that is not an integer, it will be truncated after 15 digits after the decimal place.

Strings are finite sequences of characters enclosed with double quotes (e.g. “123”, “abc”, “ar vr”, “LaG+plus”). Any ASCII character and whitespace can be put into a string.

Booleans take the form of true and false. Expressions used in loops and if statements will be evaluated into booleans (e.g. equals(1+1,2) evaluates to true, equals(1+1,3) evaluates to false) and executed accordingly.

Lists are data structures that hold ordered sequences of other types (e.g. [1,2,3], [“a”,”b”,”c”], [1,”b”,3], [], [true], [[1,2,3],[4,5,”a”],true,false,true]). Elements inside lists can be any of the four types, including other lists.

Operations

LAG++ supports addition, subtraction, multiplication, division, integer division, modulo, exponentiation, and parentheses (denoted by the symbols +,-,*,/,$,%,^,() respectively).

The modulo operation a%b denotes the remainder when a is divided by b. The integer division operation a$b works only when a and b are integers and produces the quotient of a divided by b rounded down.

In addition to all operations being usable on numbers:

Addition also works on strings (e.g. “abc” + “def” produces “abcdef”) and lists (e.g. [1,2,3] + [“a”,”b”,”c”] produces [1,2,3,”a”,”b”,”c”]).

Multiplication also works on strings multiplied by integers (e.g. “abc” * 3 produces “abcabcabc”).

In an expression with multiple operations, LAG++ will follow the established order of operations. Expressions with parentheses will be evaluated first in order from left to right, with exponentiation, followed by multiplication, division, and modulo in order from left to right, then followed by addition and subtraction in order from left to right.


Variables

In LAG++, variables are intialized in the form of variableName = value (e.g. N = 102). This creates a variable in the memory with the specified value. Variables can be deleted from the memory with the operation delete(variableName). Variables can have their values re-assigned simply by using variableName = value again. Using an expression in

In subsequent lines after the variable is declared, using the variable name in any expression in any part of the code will act as if the variable’s value was used (e.g. if N has a value of 102, then N+1 will evaluate to 102+1 which evaluates to 103).

Variables can also be modified by the following operations: += N, -= N, += N, /= N, $= N, ^= N. This will perform the requisite operation with the value N on the variable and store the resultant value into the variable. Some examples include:
If a variable N is 102, then the line N += 1 will result in the variable N becoming 103.
If a variable N is 102, then the line N -= 1 will result in the variable N becoming 101.
If a variable N is “abc”, then the line N += “def” will result in the variable N becoming “abcdef”.
If a variable N is [“a”,2,true], then the line N += [“a”] will result in the variable N becoming [“a”,2,true,”a”].

If/Else Statements

An if statement is a conditional expression that executes a certain set of statements if it evaluates to true, and does not if it evaluates to false.

If statements take the form of:
if(expression){
statements
}
If the expression evaluates to true, then the statements enclosed by the curly brackets will be executed. Otherwise, the program will skip to the first statement after the left-facing (closing) curly bracket and continue running from there.

Optionally, an else statement can be added directly after the if statement’s closing bracket. Else statements take the form:
if(expression){
statements
}
else{
statements
}
If the if statement fails, then the statements contained within the else statement will be executed, and then the code will continue on from the first line after the closing bracket of the else statement.

While Statements

The while statement is a conditional that will continuously execute its sub statements until the conditional fails. It is like an if statement, except the continuation on after the if statement is altered into going back into the conditional of the if statement.

While statements take the form of:
while(condition){
statements
}

When the program reaches the condition, it will check if the condition evaluates to true; if it does not, then it will skip to the first statement after the closing bracket and then continue on from there. If it does, it will iterate through all the statements contained within the brackets and then when the closing bracket is encountered then it will attempt to go through the conditional again; this process is repeated until the condition evaluates to false.

Optionally, there may be a statement that simply consists of break placed anywhere within the enclosing brackets of the while statement. If this statement is encountered, then the program will automatically skip to the first statement after the closing bracket in much the same way as if the conditional was evaluated to be false.

If neither break nor a false conditional is encountered, then the while statement will run infinitely or until the program is forcibly stopped by some means.

Loop Statements

The loop statement is similar to a while statement, except instead of a conditional it will loop a fixed number of times. Loop statements take the form of:
loop(variableName, minNumber, maxNumber){
statements
}

The loop statement will declare a variable named variableName, and intialize it to the value of minNumber.

It will then run the statements contained within the loop statement, and then when it reaches the closing bracket it will increase the variable by 1. It will then repeat this process until the variable’s value reaches the maxNumber, at which it will stop - it will not run the statements contained within when the variable’s value is maxNumber. Once it stops, the program will continue on from the first statement after the closing bracket.

Functions

LAG++ incorporates several functions. A function is a built-in block of code that only runs when it is called - the block of code does not need to be typed, instead only the function’s name is called and data, called parameters, is passed in. A function can return data as a result.

Functions take the form of functionName(parameter1, parameter2, … , parameterN), where N is the number of parameters.

say(expression)

The function say will print a given expression to the output. If the expression is not exactly one of the four types, it will be evaluated until it is and then printed. The expression inside can be evaluated to any one of the four types, as long as it is a valid expression.

ask(type)

The function ask will take in and return an input from the user of the given type. This function returns nothing.

get(list, index)

The function get has two parameters: the variable name of a list, and the index. It will return the Nth element of the list, where N is the index (remember that the numbering of elements in a list start from 0).

size(variable)

The function size takes in the variable name of a list or a string as its sole parameter and returns the size of the list (number of elements) or the size of the string (number of characters), respectively. It will not work with any other types.

"""


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

    master = Tk()
    master.geometry("1920x1080")
    master.title("Running")

    console = Text(master,height=90,width=90,font=("Arial",10))

    autoscroll = Scrollbar(master,command=console.yview)
    autoscroll.config(command=console.yview)

    #Reserving the rest for Adam for actual compilation of file




root = Tk()

root.geometry("1920x1080")

root.title("Lag++ Editor")

menu = Menu(root)



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