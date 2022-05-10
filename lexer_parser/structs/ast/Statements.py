from .Node import Node
from .Expressions import Assign

Statement = Node

class Globals(Statement):
    def __init__(self, estatuto, global_1):
        self.estatuto = estatuto
        self.global_1 = global_1
  
    def gen(self):
        # Checar self.estatuto.name != 'Return'
        self.estatuto.gen()
        if hasattr(self, 'global_1'):
            self.global_1.gen()

    
class Seq(Statement):
    def __init__(self, stmt, seq=None):
        self.stmt = stmt
        self.seq = seq
    
    def gen(self):
        pass


class If(Statement):
    
    class IfAux(Statement):
        def __init__(self, expr, seq):
            self.expr = expr
            self.seq = seq

        def gen(self):
            pass
    class ElseIfSeqAux(IfAux):
        def __init__(self, expr, seq, else_if_seq):
            super().__init__(expr, seq)
            self.else_if_seq = else_if_seq

        def gen(self):
            pass
    
    class ElseAux(Statement):
        def __init__(self, seq):
            self.seq = seq
        
        def gen(self):
            pass

    def __init__(self, if_aux, else_if_seq_aux=None, else_aux=None):
        self.if_aux = if_aux
        self.else_if_seq_aux = else_if_seq_aux
        self.else_aux = else_aux

    def gen(self):
        pass

class While(Statement):
    def __init__(self, expr, seq):
        self.expr = expr
        self.seq = seq

    def gen(self):
        pass

class For(Statement):
    def __init__(self, var, expr, assign, seq):
        self.var = var
        self.expr = expr
        self.assign = assign
        self.seq = seq

    def gen(self):
        pass

class VarDecl(Statement):
    def __init__(self, id, id_type):
        self.id = id
        self.id_type = id_type
        self.assign = None

    def do_assign(self, expr):
        self.assign = Assign(self.id, expr)

    def gen(self):
        pass

class FuncDecl(Statement):
    def __init__(self, id, type, params_seq, seq):
        self.id = id
        self.type = type
        self.params_seq = params_seq
        self.seq = seq 

    def gen(self):
        pass

class Ret(Statement):
    def __init__(self, expr):
        self.expr = expr

    def gen(self):
        pass