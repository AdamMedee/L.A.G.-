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
        self.graphics = False

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
        elif len(tmp) >= 4 and tmp[0:4] == "loop":
            self.readLoop(self.curLine)
        elif line == "":
            pass
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
            self.errorMessage("Curly brace in evaluation", lineNum)
        b = self.evaluate(self.code[lineNum][s+1:e+s])
        if b == "False":
            self.curLine = self.bracketChase2([lineNum, self.code[lineNum].index("{")], "{", "}")[0]
        else:
            self.goBacks[self.bracketChase2([lineNum, self.code[lineNum].index("{")], "{", "}")[0]] = self.curLine


    def commaSep(self, codel):
        tmpLis = []
        tmpstr = False
        for i in range(len(codel)):
            if codel[i] == '"':
                tmpstr = not tmpstr
            elif codel[i] == "," and tmpstr:
                codel = codel[:i] + "企" + codel[i + 1:]
        for thing in codel.split(","):
            tmpLis.append(self.evaluate(thing.replace("企", ",")))
        return tmpLis

    def readLoop(self, lineNum):
        s = self.code[lineNum].find("(")
        e = self.bracketChase(self.code[lineNum][s:], "(", ")")
        abc = self.code[lineNum][s+1:s+e].replace(" ", "")
        name, strt, end = self.commaSep(abc[1:len(abc)-1])

        if name not in self.vars.keys():
            self.vars[name] = int(strt)
        else:
            self.vars[name] += 1
        if "{" in self.code[lineNum] and s <= self.code[lineNum].find("{") <= e:
            self.errorMessage("Curly brace in evaluation", lineNum)
        b = self.evaluate(name + "<" + end)
        if b == "False":
            del self.vars[name]
            self.curLine = self.bracketChase2([lineNum, self.code[lineNum].index("{")], "{", "}")[0]
        else:
            self.goBacks[self.bracketChase2([lineNum, self.code[lineNum].index("{")], "{", "}")[0]] = self.curLine


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
        if ("[" in codel or "]" in codel) and (codel[0] != "[" or codel[-1] != "]"):
            self.errorMessage("List literal in evaluation", codel)
        if "[" in codel and "]" in codel and codel[0] == "[" and codel[-1] == "]":
            tmpLis = []
            tmpstr = False
            for i in range(len(codel)):
                if codel[i] == '"':
                    tmpstr = not tmpstr
                elif codel[i] == "," and tmpstr:
                    codel = codel[:i]+"企"+codel[i+1:]
            for thing in codel[1:len(codel)-1].split(","):
                tmpLis.append(self.evaluate(thing.replace("企", ",")))
            return tmpLis


        #Remove brackets except for function calls
        s = 0
        while True:
            if "(" not in codel[s:]:
                break
            s = codel[s:].index("(")+s
            if s == 0 or codel[s-1] not in "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm":
                e = self.bracketChase(codel[s:], "(", ")")
                a = codel[:s]
                if a == None:
                    a = ""
                b = codel[e+s+1:]
                if b == None:
                    b = ""
                codel = a + self.evaluate(codel[s+1:e+s]) + b
                s += 1
            elif codel[s-1] in "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm":
                s += 1
            if s == len(codel)-1:
                break

        inBracks = 0
        inStr = False
        for ops in self.orderofops:
            for o in ops:
                i = 0
                while i < len(codel):
                    if codel[i] == "(":
                        inBracks+=1
                    elif codel[i] == ")":
                        inBracks-=1
                    elif codel[i] == '"':
                        inStr = not inStr
                    if codel[i] == o and inBracks == 0 and not inStr:
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
                    printed = self.evaluate(cod[s+1:s+e])
                    if self.getType(printed) == "list":
                        self.output(printed)
                    else:
                        self.output(self.evaluate(cod[s+1:s+e]))
                    return "True"
                elif cod[:s] == "ask":
                    return self.l_input()
                elif cod[:s] == "get":
                    l, pos = self.commaSep(cod[s+1:s+e])
                    return self.vars[cod[s+1:s+e][:cod[s+1:s+e].index(",")]][int(pos)]
                elif cod[:s] == "set":
                    l, pos, val = self.commaSep(cod[s+1:s+e])
                    self.vars[cod[s+1:s+e][:cod[s+1:s+e].index(",")]][int(pos)] = val
                    return "True"
                elif cod[:s] == "add":
                    l, item = self.commaSep(cod[s+1:s+e])
                    self.vars[cod[s + 1:s + e][:cod[s + 1:s + e].index(",")]].append(item)
                    return "True"
                elif cod[:s] == "size":
                    return str(len(self.vars[cod[s+1:s+e]]))
                elif cod[:s] == "del":
                    l, ind = self.commaSep(cod[s+1:s+e])
                    del self.vars[cod[s + 1:s + e][:cod[s + 1:s + e].index(",")]][int(ind)]
                    return "True"
                elif cod[:s] == "makeScreen":
                    w, h = self.commaSep(cod[s+1:s+e])
                    self.makeScreen(int(w), int(h))
                    return "True"
                elif cod[:s] == "Event":
                    self.checkEvents()
                elif cod[:s] == "DrawRect":
                    col, x, y, w, h, t = self.commaSep(cod[s+1:s+e])
                    self.drawRect([x, y, w, h], col, t)

            elif cod in self.vars.keys():
                codeList[i] = str(self.vars[cod])



        while len(codeList) != 1:
            for ops in self.orderofops:
                f = 999999999
                for o in ops:
                    if o in codeList:
                        f = min(f, codeList.index(o))
                if f != 999999999:
                    if f == 0 or f == len(codeList)-1:
                        self.errorMessage("Operation is not connecting two things", (codel, f))
                    codeList[f] = self.evaluate2(codeList[f-1], codeList[f], codeList[f+1])
                    del codeList[f+1]
                    del codeList[f-1]

        return codeList[0]

    #Starting graphics
    def makeScreen(self, w, h):
        width, height = w, h
        init()
        self.screen = display.set_mode((width, height))
        self.graphics = True

    def checkEvents(self):
        for action in event.get():
            if action.type == QUIT:
                quit()
        display.flip()

    def fillBg(self, col):
        self.screen.fill(self.h2r(col))

    def drawLine(self, p1, p2, col, thickness):
        draw.line(self.screen, self.h2r(col), [int(c) for c in p1], [int(c) for c in p2], int(thickness))

    def drawRect(self, r, col, thickness):
        draw.rect(self.screen, self.h2r(col), [int(c) for c in r], int(thickness))

    def drawEllipse(self, r, col, thickness):
        draw.ellipse(self.screen, self.h2r(col), [int(c) for c in r], int(thickness))

    def drawCirc(self, p1, rad, col, thickness):
        draw.circle(self.screen, self.h2r(col), [int(c) for c in p1], int(rad),int(thickness))

    def h2r(self, value):
        value = value[1:len(value)-1]
        vals = "0123456789abcdef"
        lv = len(value)
        return ((vals.index(value[0])*16+vals.index(value[1])), (vals.index(value[2])*16+vals.index(value[3])), (vals.index(value[4])*16+vals.index(value[5])),)

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
        print(msg.replace("磨", " "))

    def l_input(self):
        pass

    def func(self, term):
        f = term[:term.index("(")]
        if f == "say":
            self.output(term[(term.index("(")+1):(term.index(")")+1)])


co = [
   "nums = [1, 2, 3]",
    "say(get(nums, 1))",
    "set(nums, 1, 5)",
    "say(size(nums))",
    "add(nums, 17)",
    "say(nums)",
    "del(nums, 3)",
    "say(nums)",
    "makeScreen(800, 400)",
    "while(True){",
    "Event()",
    'DrawRect("ff0000", 100, 200, 400, 450, 2)',
    "}"
]


