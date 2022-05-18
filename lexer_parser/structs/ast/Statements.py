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
            var = self.expr.gen(ctx)
            gotof_index = ctx.add_quadruple(Quadruple('GOTOF', var.name))
            ctx.func_dir.start_block_stack()
            self.seq.gen(ctx)
            ctx.func_dir.end_block_stack()
            return gotof_index

    class ElseIfSeqAux(IfAux):
        def __init__(self, expr, seq, else_if_seq):
            super().__init__(expr, seq)
            self.else_if_seq = else_if_seq

        def gen(self, ctx: ParseContext, if_goto_index):
            # gen goto to jump this when prev block is executed
            end_goto_index = ctx.add_quadruple(Quadruple('GOTO'))
            # fill gotof of previous if expr
            ctx.set_goto_position(if_goto_index)
            # gens expr qs, gotof q, block qs, and returns location of gotof
            gotof_index = super().gen(ctx)
    
            if isinstance(self.else_if_seq, Empty):
                return [gotof_index, end_goto_index]
  
            # Gen qs for all remaining else ifs, which return their end goto_index
            goto_array = self.else_if_seq.gen(ctx, gotof_index)
            return [end_goto_index] + goto_array
    
    class ElseAux(Statement):
        def __init__(self, seq):
            self.seq = seq
        
        def gen(self, ctx: ParseContext):
            end_goto_index = ctx.add_quadruple(Quadruple('GOTO'))
            ctx.func_dir.start_block_stack()
            self.seq.gen(ctx)
            ctx.func_dir.end_block_stack()
            ctx.set_goto_position(end_goto_index)

    def __init__(self, if_aux, else_if_seq_aux=Empty(), else_aux=Empty()):
        self.if_aux = if_aux
        self.else_if_seq_aux = else_if_seq_aux
        self.else_aux = else_aux

    def gen(self, ctx: ParseContext):
        goto_array = []
        if_gotof_index = self.if_aux.gen(ctx)
        if not isinstance(self.else_if_seq_aux, Empty):
            goto_array = self.else_if_seq_aux.gen(ctx, if_gotof_index)
        
        self.else_aux.gen(ctx)
        
        if isinstance(self.else_if_seq_aux, Empty): 
            ctx.set_goto_position(if_gotof_index)
        for goto_index in goto_array:
            ctx.set_goto_position(goto_index)

class While(Statement):
    def __init__(self, expr, seq):
        self.expr = expr
        self.seq = seq

    def gen(self, ctx: ParseContext):
        jump_index = ctx.get_next_quadruple_index()
        var = self.expr.gen(ctx)
        gotof_index = ctx.add_quadruple(Quadruple('GOTOF', var.name))
        ctx.func_dir.start_block_stack()
        self.seq.gen(ctx)
        ctx.func_dir.end_block_stack()
        ctx.add_quadruple(Quadruple('GOTO',result=jump_index))
        ctx.set_goto_position(gotof_index)

class For(Statement):
    def __init__(self, var, expr, assign, seq=Empty()):
        self.var = var
        self.expr = expr
        self.assign = assign
        self.seq = seq

    def gen(self, ctx: ParseContext): 
        ctx.func_dir.start_block_stack()
        self.var.gen(ctx)
        jump_index = ctx.get_next_quadruple_index()
        var = self.expr.gen(ctx)
        gotof_index = ctx.add_quadruple(Quadruple('GOTOF', var.name))
        self.seq.gen(ctx)
        self.assign.gen(ctx)
        ctx.add_quadruple(Quadruple('GOTO', result=jump_index))
        ctx.set_goto_position(gotof_index)
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
        print('gen decl')
        self.id.set_id_type(self.id.id, self.id_type)
        var = ctx.func_dir.add_var(self.id.id, self.id_type)
        self.assign.gen(ctx)
        return var
        # do stuff

class FuncDecl(Statement):
    def __init__(self, id, id_type, params_seq, seq):
        self.id = id
        assert Expression in type(id).__mro__
        self.id_type = id_type
        self.params_seq = params_seq
        self.seq = seq 

    def gen(self, ctx: ParseContext):
        goto_index = ctx.add_quadruple(Quadruple('GOTO')) # add gotos to skip function on initial execution, only executed once called
        
        self.id.set_id_type(self.id.id, self.id_type)
        
        q_index = goto_index+1 # index for starting at func
        ctx.func_dir.start_func_stack(self.id.id, self.id_type, q_index)
        vars = self.params_seq.gen(ctx)
        print('decl vars ', vars)
        ctx.func_dir.set_func_params([] if vars == None else vars)
        ctx.add_quadruple(Quadruple('ERA',result=self.id.id)) # on vm lookup func by id
        self.seq.gen(ctx)
        ctx.func_dir.end_func_stack(self.id.id)
        ctx.add_quadruple(Quadruple('ENDFUNC'))
        ctx.set_goto_position(goto_index) # fill goto

class Ret(Statement):
    def __init__(self, expr):
        self.expr = expr

    def gen(self, ctx: ParseContext):
        self.expr.gen(ctx)

class FuncCall(Statement):
    def __init__(self, id, args_seq):
        self.id = id
        self.args_seq = args_seq
    
    def gen(self, ctx: ParseContext):
        func = ctx.func_dir.get_func(self.id)
        vars = self.args_seq.gen(ctx)
        vars = [] if vars == None else vars 
        print('vars ', vars)
        print('func.params ', func.params)
        next_q = ctx.get_next_quadruple_index() + 1
        ctx.add_quadruple(Quadruple('GOSUB', next_q, result=func.name))
        assert len(vars) == len(func.params)
        for (i, var) in enumerate([] if vars == None else vars):
            param = func.params[i]
            ctx.semantic_cube.get_type('ASSIG', param.type, var.type)
            ctx.add_quadruple(Quadruple('PARAM', var.name, result=param.name))


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
            