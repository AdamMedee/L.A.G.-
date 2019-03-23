from pygame import *
from math import *

class Code:
    def __init__(self, code):
        self.code = code
        self.curline = 0
        self.vars = {}
        self.const = {}
        self.operations = ["+", "-", "*", "/", "%", "//", "^"]

    def runLine(self):
        pass

    def bracketChase(self, pos, t1, t2):
        count = 1
        orig = pos
        while True:
            if (pos[1]+1) == len(self.code[pos[0]]):
                pos[1] = 0
            else:
                pos[1] += 1
            if self.code[pos[0]][pos[1]] == "t2":
                count -= 1
            elif self.code[pos[0]][pos[1]] == "t1":
                count += 1
            if count == 0:
                return pos
            elif pos[0]+1 == len(self.code) and pos[1]+1 == len(self.code[pos[0]]):
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
        pass

    def errorMessage(self, error, info):
        pass

    def output(self, msg):
        print(msg)

    def l_input(self):
        pass