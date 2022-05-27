
class Quadruple():
    def __init__(self, op, arg_1=None, arg_2=None, result=None):
        self.op = op
        self.arg_1 = arg_1
        self.arg_2 = arg_2
        self.result = result
    
    def __repr__(self) -> str:
        return f"Q({self.op}, {self.arg_1}, {self.arg_2}, {self.result})"

    def to_ir_repr(self):
        return (self.op, self.arg_1, self.arg_2, self.result)