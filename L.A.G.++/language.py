from pygame import *
from math import *

class Code:
    def __init__(self, code):
        self.code = code
        self.curline = 0
        self.vars = {}
        self.const = {}
        self.predef = ["+", "-", "*", "/", "%", "$", "^", "and", "or", "if", "loop", "while", "xor"]
        self.orderofops = [["^"], ["*", "/", "$", "%"], ["+", "-"], ["and"], ["or", "xor"]]

    def run(self):
        self.curLine = 0
        while self.curLine != len(self.code):
            self.runLine(self.curLine)
            self.curLine += 1

    def runLine(self, line):
        if "=" in line:
            self.defineVar(line)
        else:
            self.evaluate(line)

    def bracketChase(self, pos, t1, t2):
        count = 1
        orig = pos
        while True:
            if (pos[1]+1) == len(self.code[pos[0]]):
                pos[1] = 0
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
        count = 1
        orig = 1
        while True:
            if code[orig] == t2:
                count -= 1
            elif code[orig] == t1:
                count += 1
            if count == 0:
                return orig
            orig += 1
            if code[orig]+1 == len(code):
                self.errorMessage("Missing End Bracket", orig)
                break

    def defineVar(self, line):
        a, b = line.split("=")
        self.vars[a] = self.evaluate(b)

    def changeVar(self, line, op):
        a, b = line.split(op+"=")
        if a in self.vars.keys():
            self.vars[a] = self.evaluate(b)
        else:
            self.errorMessage("Variable Not Defined", a)

    def readIf(self, lineNum):
        s = self.code[lineNum].find("(")


    def evaluate(self, code):
        if "[" in code:
            self.bracketChase(code, "[", "]")
        if "[" in code or "]" in code and (code[0] != "[" or code[-1] != "]"):
            self.errorMessage("List literal in evaluation", code)
        if "[" in code and "]" in code and code[0] == "[" and code[-1] == "]":
            return code
        if "(" in code:
            s = code.find("(")
            e = self.bracketChase(code, "(", ")")
            code = code[:s] + self.evaluate(code[s:e]) + code[e:]
        for ops in self.orderofops:
            for o in ops:
                if o in self.code:
                    self.code = self.code[:code.find(o)] + " " + o + " " + self.code[code.find(o):]
        codeList = self.code.split()
        while len(codeList) != 1:
            for ops in self.orderofops:
                f = 999999999
                for o in ops:
                    if o in code:
                        f = min(f, codeList.index(o))
                if f != 999999999:
                    if f == 0 or f == len(codeList-1):
                        self.errorMessage("Operation is not connecting two things", (code, f))
                    codeList[f] = self.evaluate2(codeList[f-1], codeList[f], codeList[f+1])
                    del codeList[f+1]
                    del codeList[f-1]
        return codeList[0]

    def evaluate2(self, x, o, y):
        if self.getType(x) == self.getType(y) == "num":
            if x % 1 == 0:
                x = int(x)
            else:
                x = float(x)
            if y % 1 == 0:
                y = int(y)
            else:
                y = float(y)
            if o == "+":
                return x+y
            elif o == "-":
                return x-y
            elif o == "*":
                return x*y
            elif o == "/":
                return x/y
            elif o == "^":
                return x**y
            elif o == "$":
                return x//y
            elif o == "%":
                return x%y
        if self.getType(x) == self.getType(y) == "str":
            if o == "+":
                return '"'+x[1:len(x)-1]+y[1:len(y)-1]+'"'
        if self.getType(x) == "num" and self.getType(y) == "str":
            if x % 1 == 0:
                x = int(x)
            else:
                x = float(x)
            y = y[1:len(y)-1]
            if o == "*":
                if x%1 != 0:
                    self.errorMessage("Can't multiply a string by a non-integer", (x, y))
                return x*y
        if self.getType(y) == "num" and self.getType(x) == "str":
            if y % 1 == 0:
                y = int(y)
            else:
                y = float(y)
            x = x[1:len(x)-1]
            if o == "*":
                if y%1 != 0:
                    self.errorMessage("Can't multiply a string by a non-integer", (y, x))
                return x*y
        if self.getType(x) == "bool" and self.getType(y) == "bool":
            if o == "and":
                return bool(x) and bool(y)
            elif o == "or":
                return bool(x) or bool(y)
            elif o == "xor":
                return bool(x) ^ bool(y)




    def getType(self, code):
        try:
            code = int(code)
            return "num"
        except:
            pass
        if code[1] == code[-1] == '"':
            return "str"
        if code == "True" or code == "False":
            return "bool"
        if code[0] == "[" and code[-1] == "]":
            return "list"
        self.errorMessage("Type Unknown", code)


    def errorMessage(self, error, info):
        return 0

    def output(self, msg):
        print(msg)

    def l_input(self):
        pass



