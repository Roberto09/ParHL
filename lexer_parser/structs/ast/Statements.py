from ..quadruples import Quadruple
from ..parse_context import ParseContext
from .Node import Node
from .Expressions import Assign, Expression

Statement = Node

type_to_token = {
    'int': 'INT_T',
    'float': 'FLOAT_T',
    'string': 'STRING_T', 
    'bool': 'BOOL_T',
    'gpu_int': 'GPU_INT_T',
    'gpu_float': 'GPU_FLOAT_T',
    'gpu_bool': 'GPU_BOOL_T'
}

class Empty(Statement):
    def __init__(self):
        pass
    def gen(self, ctx: ParseContext):
        pass
    
class Seq(Statement):
    def __init__(self, stmt, seq=Empty()):
        self.stmt = stmt
        self.seq = seq

    def gen(self, ctx: ParseContext):
        try:
            first = self.stmt.gen(ctx)
        except:
            print(self.stmt)
            raise
        second = self.seq.gen(ctx)
        if first == None and second == None:
            return []
        elif second == None:
            return [first]
        elif first == None:
            return second
        else:
            return [first] + second

class If(Statement):
    
    class IfAux(Statement):
        def __init__(self, expr, seq):
            self.expr = expr
            self.seq = seq

        def gen(self, ctx: ParseContext):
            self.expr.gen(ctx)
            ctx.func_dir.start_block_stack()
            self.seq.gen(ctx)
            ctx.func_dir.end_block_stack()
    class ElseIfSeqAux(IfAux):
        def __init__(self, expr, seq, else_if_seq):
            super().__init__(expr, seq)
            self.else_if_seq = else_if_seq

        def gen(self, ctx: ParseContext):
            super().gen(ctx)
            self.else_if_seq.gen(ctx)
    
    class ElseAux(Statement):
        def __init__(self, seq):
            self.seq = seq
        
        def gen(self, ctx: ParseContext):
            ctx.func_dir.start_block_stack()
            self.seq.gen(ctx)
            ctx.func_dir.end_block_stack()

    def __init__(self, if_aux, else_if_seq_aux=Empty(), else_aux=Empty()):
        self.if_aux = if_aux
        self.else_if_seq_aux = else_if_seq_aux
        self.else_aux = else_aux

    def gen(self, ctx: ParseContext):
        self.if_aux.gen(ctx)
        self.else_if_seq_aux.gen(ctx)
        self.else_aux.gen(ctx)

class While(Statement):
    def __init__(self, expr, seq):
        self.expr = expr
        self.seq = seq

    def gen(self, ctx: ParseContext):
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

    def gen(self, ctx: ParseContext): 
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
        self.id_type = type_to_token[id_type]
        self.assign = Empty()

    def do_assign(self, expr):
        self.assign = Assign(self.id, expr)

    def gen(self, ctx: ParseContext):
        self.id.set_id_type(self.id.id, self.id_type)
        ctx.func_dir.add_var(self.id.id, self.id_type)
        self.assign.gen(ctx)
        # do stuff

class FuncDecl(Statement):
    def __init__(self, id, id_type, params_seq, seq):
        self.id = id
        assert Expression in type(id).__mro__
        self.id_type = id_type
        self.params_seq = params_seq
        self.seq = seq 

    def gen(self, ctx: ParseContext):
        self.id.set_id_type(self.id.id, self.id_type)
        ctx.func_dir.start_func_stack(self.id.id, self.id_type)
        self.params_seq.gen(ctx)
        self.seq.gen(ctx)
        ctx.func_dir.end_func_stack(self.id.id)

class Ret(Statement):
    def __init__(self, expr):
        self.expr = expr

    def gen(self, ctx: ParseContext):
        self.expr.gen(ctx)

class FuncCall(Statement):
    def __init__(self, id, args_seq = Empty()):
        self.id = id
        self.args_seq = args_seq
    
    def gen(self, ctx: ParseContext):
        self.args_seq.gen(ctx)

class IOFunc(FuncCall):
    def __init__(self, id, args_seq=Empty()):
        super().__init__(id, args_seq)
    
    def gen(self, ctx: ParseContext):
        seq = self.args_seq.gen(ctx)
        if self.id in 'read_line':
            new_var = ctx.func_dir.new_temp('STRING_T')
            ctx.add_quadruple(Quadruple('READ_LINE', None, None, new_var.name))
            return new_var
        if self.id == 'read_file' and seq is not None:
            new_var = ctx.func_dir.new_temp('STRING_T')
            ctx.add_quadruple(Quadruple('READ_FILE', seq[0].name, None, new_var.name))
            return new_var
        if seq == None:
            seq = []
        for arg in seq:
            ctx.add_quadruple(Quadruple(self.id.upper(), None, None, arg.name))
            