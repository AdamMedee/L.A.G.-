from pygame import *
from math import *

class Code:
    def __init__(self, code):
        self.code = code
        self.curline = 0
        self.vars = {}
        self.const = {}

    def runLine(self):
        pass

    def bracketChase(self, pos, t1, t2):
        count = 1
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


    def errorMessage(self, error):
        pass

    def output(self, msg):
        print(msg)
