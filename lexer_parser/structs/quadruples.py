from enum import Enum, unique

@unique
class QOps(Enum): # Current next: 18
    PLUS = 1
    MINUS = 2
    DIV = 3
    MULT = 4
    EXP = 5
    MOD = 6
    ASSIG = 7
    EQ = 8
    NOT_EQ = 9
    GEQT = 10
    LEQT = 11
    GT = 12
    LT = 13
    PRINT = 14
    READ_LINE = 15
    READ_FILE = 16
    WRITE_FILE = 17

class Quadruple():
    def __init__(self, op: QOps, arg_1, arg_2, result):
        self.op = op
        self.arg_1 = arg_1
        self.arg_2 = arg_2
        self.result = result