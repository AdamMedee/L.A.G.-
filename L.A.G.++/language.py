from pygame import *
from math import *

class Code:
    def __init__(self, code):
        self.code = code
        self.curline = 0
        self.vars = {}
        self.const = {}
        self.predef = ["+", "-", "*", "/", "%", "$", "^", "and", "or", "if", "loop", "while", "xor"]
        self.orderofops = [["^"], ["*", "/", "$", "%"], ["+", "-"], ["<", ">", "~"], ["and"], ["or", "xor"]]
        self.goBacks = {}

    def run(self):
        self.curLine = 0
        while self.curLine != len(self.code):
            self.runLine(self.code[self.curLine])
            self.curLine += 1

    def runLine(self, line):
        tmp = line.replace(" ", "")
        if "=" in line and line[line.index("=")-1] not in "+-*/%$^":
            self.defineVar(line)
        elif "+=" in line:
            self.changeVar(line, "+")
        elif "-=" in line:
            self.changeVar(line, "-")
        elif "*=" in line:
            self.changeVar(line, "*")
        elif "}" in line:
            if self.curLine in self.goBacks.keys():
                a = self.goBacks[self.curLine]
                del self.goBacks[self.curLine]
                self.curLine = a-1
        elif len(tmp) >= 2 and tmp[0]+tmp[1] == "if":
            self.readIf(self.curLine)
        elif len(tmp) >= 5 and tmp[0:5] == "while":
            self.readWhile(self.curLine)
        else:
            self.evaluate(line)

    def bracketChase2(self, pos, t1, t2):
        count = 1
        orig = pos
        while True:
            if (pos[1]+1) == len(self.code[pos[0]]):
                pos[1] = 0
                pos[0] += 1
            else:
                pos[1] += 1
            if self.code[pos[0]][pos[1]] == t2:
                count -= 1
            elif self.code[pos[0]][pos[1]] == t1:
                count += 1
            if count == 0:
                return pos
            elif pos[0]+1 == len(self.code) and pos[1]+1 == len(self.code[pos[0]]):
                self.errorMessage("Missing End Bracket", orig)
                break

    def bracketChase(self, code, t1, t2):
        count = 0
        orig = -1
        while True:
            orig += 1
            if code[orig] == t2:
                count -= 1
            elif code[orig] == t1:
                count += 1
            if count == 0:
                return orig
            if orig+1 == len(code):
                self.errorMessage("Missing End Bracket", orig)
                break


    def defineVar(self, line):
        a, b = line.split("=")
        a = a.replace(" ", "")
        self.vars[a] = self.evaluate(b)


    def changeVar(self, line, op):
        a, b = line.split(op+"=")
        a = a.replace(" ", "")
        if a in self.vars.keys():
            self.vars[a] = self.evaluate(a+op+self.evaluate(b))
        else:
            self.errorMessage("Variable Not Defined", a)


    def readIf(self, lineNum):
        s = self.code[lineNum].find("(")
        e = self.bracketChase(self.code[lineNum][s:], "(", ")")
        if "{" in self.code[lineNum] and s <= self.code[lineNum].find("{") <= e:
            self.errorMessage("Curly brace in evaluation")
        b = self.evaluate(self.code[lineNum][s+1:e+s])
        if b == "False":
            self.curLine = self.bracketChase2([lineNum, self.code[lineNum].index("{")], "{", "}")[0]

    def readWhile(self, lineNum):
        s = self.code[lineNum].find("(")
        e = self.bracketChase(self.code[lineNum][s:], "(", ")")
        if "{" in self.code[lineNum] and s <= self.code[lineNum].find("{") <= e:
            self.errorMessage("Curly brace in evaluation")
        b = self.evaluate(self.code[lineNum][s+1:e+s])
        if b == "False":
            self.curLine = self.bracketChase2([lineNum, self.code[lineNum].index("{")], "{", "}")[0]
        else:
            self.goBacks[self.bracketChase2([lineNum, self.code[lineNum].index("{")], "{", "}")[0]] = self.curLine



    def readFor(self, lineNum):
        pass


    #Recursively evals a statement
    def evaluate(self, codel):
        #Removing spaces
        instr = False
        for i in range(len(codel)-1, -1, -1):
            if codel[i] == '"':
                instr = not instr
            if not instr and codel[i] == " ":
                codel = codel[:i] + codel[i+1:]
            elif instr and codel[i] == " ":
                codel = codel[:i] + "磨" + codel[i+1:]

        #Lists for vals
        if "[" in codel:
            self.bracketChase(codel, "[", "]")
        if "[" in codel or "]" in codel and (codel[0] != "[" or codel[-1] != "]"):
            self.errorMessage("List literal in evaluation", codel)
        if "[" in codel and "]" in codel and codel[0] == "[" and codel[-1] == "]":
            return codel

        #Remove brackets except for function calls
        s = 0
        while True:
            if "(" not in codel[s:]:
                break
            s = codel[s:].index("(")
            if s == 0 or codel[s-1] not in "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm":
                e = self.bracketChase(codel[s:], "(", ")")
                a = codel[:s]
                if a == None:
                    a = ""
                b = codel[e+s+1:]
                if b == None:
                    b = ""
                codel = a + self.evaluate(codel[s+1:e+s]) + b
            elif codel[s-1] in "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm":
                s += 1

        inBracks = 0
        for ops in self.orderofops:
            for o in ops:
                i = 0
                while i < len(codel):
                    if codel[i] == "(":
                        inBracks+=1
                    elif codel[i] == ")":
                        inBracks-=1
                    if codel[i] == o and inBracks == 0:
                        codel = codel[:i] + " " + o + " " + codel[i+1:]
                        i += 1
                    i += 1


        codeList = codel.split()

        for i in range(len(codeList)):
            cod = codeList[i]
            if "(" in cod:
                s = cod.index("(")
                e = self.bracketChase(cod[s:], "(", ")")
                if cod[:s] == "say":
                    self.output(self.evaluate(cod[s+1:s+e]))
                    return "None"
            elif cod in self.vars.keys():
                codeList[i] = str(self.vars[cod])




        while len(codeList) != 1:
            for ops in self.orderofops:
                f = 999999999
                for o in ops:
                    if o in codel:
                        f = min(f, codeList.index(o))
                if f != 999999999:
                    if f == 0 or f == len(codeList)-1:
                        self.errorMessage("Operation is not connecting two things", (codel, f))
                    codeList[f] = self.evaluate2(codeList[f-1], codeList[f], codeList[f+1])
                    del codeList[f+1]
                    del codeList[f-1]

        return codeList[0]


    #Takes two things and a binary operation and evals it
    def evaluate2(self, x, o, y):
        if self.getType(x) == self.getType(y) == "num":
            if float(x) % 1 == 0:
                x = int(x)
            else:
                x = float(x)
            if float(y) % 1 == 0:
                y = int(y)
            else:
                y = float(y)
            if o == "+":
                return str(x+y)
            elif o == "-":
                return str(x-y)
            elif o == "*":
                return str(x*y)
            elif o == "/":
                return str(x/y)
            elif o == "^":
                return str(x**y)
            elif o == "$":
                return str(x//y)
            elif o == "%":
                return str(x%y)
            elif o == "~":
                return str(x==y)
            elif o == ">":
                return str(x>y)
            elif o == "<":
                return str(x<y)
        if self.getType(x) == self.getType(y) == "str":
            if o == "+":
                return '"'+x[1:len(x)-1]+y[1:len(y)-1]+'"'
        if self.getType(x) == "num" and self.getType(y) == "str":
            if float(x) % 1 == 0:
                x = int(x)
            else:
                x = float(x)
            y = y[1:len(y)-1]
            if o == "*":
                if x%1 != 0:
                    self.errorMessage("Can't multiply a string by a non-integer", (x, y))
                return '"' + x*y + '"'
        if self.getType(y) == "num" and self.getType(x) == "str":
            if float(y) % 1 == 0:
                y = int(y)
            else:
                y = float(y)
            x = x[1:len(x)-1]
            if o == "*":
                if y%1 != 0:
                    self.errorMessage("Can't multiply a string by a non-integer", (y, x))
                return '"' + x*y + '"'
        if self.getType(x) == "bool" and self.getType(y) == "bool":
            if o == "and":
                return str(bool(x) and bool(y))
            elif o == "or":
                return str(bool(x) or bool(y))
            elif o == "xor":
                return str(bool(x) ^ bool(y))





    def getType(self, code):
        try:
            code = int(code)
            return "num"
        except:
            pass
        if code[0] == code[-1] == '"':
            return "str"
        if code == "True" or code == "False":
            return "bool"
        if code[0] == "[" and code[-1] == "]":
            return "list"
        self.errorMessage("Type Unknown", code)


    def errorMessage(self, error, info):
        print(error, info)

    def output(self, msg):
        print(msg)

    def l_input(self):
        pass

    def func(self, term):
        f = term[:term.index("(")]
        if f == "say":
            self.output(term[(term.index("(")+1):(term.index(")")+1)])


co = [
   "x = 2  ",
    "z = 4",
    'y =(2*(3 + 4)*2)*  ("hi" + "he y")',
    "  say (y)",
    "while(z < 20){",
    "z += 2",
    "say(z+2)",
    "}",
    "say(z)",
    ""
]
c = Code(co)

c.run()