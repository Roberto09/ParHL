from .Node import Node
from .Expressions import Assign, Expression

Statement = Node

class Empty(Statement):
    def __init__(self):
        pass
    def gen(self, ctx):
        pass
    
class Seq(Statement):
    def __init__(self, stmt, seq=Empty()):
        self.stmt = stmt
        self.seq = seq

    def gen(self, ctx):
        try:
            self.stmt.gen(ctx)
        except:
            print(self.stmt)
            raise
        self.seq.gen(ctx)

class If(Statement):
    
    class IfAux(Statement):
        def __init__(self, expr, seq):
            self.expr = expr
            self.seq = seq

        def gen(self, ctx):
            self.expr.gen(ctx)
            ctx.func_dir.start_block_stack()
            self.seq.gen(ctx)
            ctx.func_dir.end_block_stack()
    class ElseIfSeqAux(IfAux):
        def __init__(self, expr, seq, else_if_seq):
            super().__init__(expr, seq)
            self.else_if_seq = else_if_seq

        def gen(self, ctx):
            super().gen(ctx)
            self.else_if_seq.gen(ctx)
    
    class ElseAux(Statement):
        def __init__(self, seq):
            self.seq = seq
        
        def gen(self, ctx):
            ctx.func_dir.start_block_stack()
            self.seq.gen(ctx)
            ctx.func_dir.end_block_stack()

    def __init__(self, if_aux, else_if_seq_aux=Empty(), else_aux=Empty()):
        self.if_aux = if_aux
        self.else_if_seq_aux = else_if_seq_aux
        self.else_aux = else_aux

    def gen(self, ctx):
        self.if_aux.gen(ctx)
        self.else_if_seq_aux.gen(ctx)
        self.else_aux.gen(ctx)

class While(Statement):
    def __init__(self, expr, seq):
        self.expr = expr
        self.seq = seq

    def gen(self, ctx):
        self.expr.gen(ctx)
        ctx.func_dir.start_block_stack()
        self.seq.gen(ctx)
        ctx.func_dir.end_block_stack()

class For(Statement):
    def __init__(self, var, expr, assign, seq):
        self.var = var
        self.expr = expr
        self.assign = assign
        self.seq = seq

    def gen(self, ctx): 
        ctx.func_dir.start_block_stack()
        self.var.gen(ctx)
        self.expr.gen(ctx)
        self.assign.gen(ctx)
        self.seq.gen(ctx)
        ctx.func_dir.end_block_stack()

class VarDecl(Statement):
    def __init__(self, id, id_type):
        self.id = id
        assert Expression in type(id).__mro__
        self.id_type = id_type
        self.assign = Empty()

    def do_assign(self, expr):
        self.assign = Assign(self.id, expr)

    def gen(self, ctx):
        self.id.set_id_type(self.id.id, self.id_type)
        ctx.func_dir.add_var(self.id.id, self.id_type)
        # do stuff

class FuncDecl(Statement):
    def __init__(self, id, id_type, params_seq, seq):
        self.id = id
        assert Expression in type(id).__mro__
        self.id_type = id_type
        self.params_seq = params_seq
        self.seq = seq 

    def gen(self, ctx):
        self.id.set_id_type(self.id.id, self.id_type)
        ctx.func_dir.start_func_stack(self.id.id, self.id_type)
        self.params_seq.gen(ctx)
        self.seq.gen(ctx)
        ctx.func_dir.end_func_stack(self.id.id)

class Ret(Statement):
    def __init__(self, expr):
        self.expr = expr

    def gen(self, ctx):
        self.expr.gen(ctx)

class FuncCall(Statement):
    def __init__(self, id, args_seq = Empty()):
        self.id = id
        self.args_seq = args_seq
    
    def gen(self, ctx):
        self.args_seq.gen(ctx)

class IOFunc(FuncCall):
    def __init__(self, id, args_seq=Empty()):
        super().__init__(id, args_seq)
    
    def gen(self, ctx):
        self.args_seq.gen(ctx)