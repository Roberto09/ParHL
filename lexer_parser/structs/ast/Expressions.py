from ast import Expression
from .Node import Node
from ..parse_context import ParseContext
from ..quadruples import Quadruple
from ...lexer import symbol_to_token

Expression = Node

class Assign(Expression):
    def __init__(self, line, left, right):
        super().__init__(line)
        self.left = left
        self.right = right
  
    def gen_impl(self, ctx: ParseContext):
        right_var = self.right.gen(ctx)
        left_var = self.left.gen(ctx)
        ctx.semantic_cube.get_type('ASSIG',left_var.type, right_var.type)
        ctx.add_quadruple(Quadruple('ASSIG', right_var.mem_dir, None, left_var.mem_dir))


class BinExpr(Expression):
    def __init__(self, line, left, op, right): 
        super().__init__(line)
        self.left = left
        self.right = right
        self.op = op

    def gen_impl(self, ctx: ParseContext):
        left_var = self.left.gen(ctx)
        right_var = self.right.gen(ctx)
        op_name = symbol_to_token[self.op]
        new_type = ctx.semantic_cube.get_type(op_name, left_var.type, right_var.type)
        temp_var = ctx.func_dir.new_temp(new_type)
        # Need to change names to mem_dirs when they are functioning
        ctx.add_quadruple(Quadruple(op_name, left_var.mem_dir, right_var.mem_dir, temp_var.mem_dir))
        return temp_var


# This implementation depends a bit on how we actually want to handle
# constants in memory and in quadruples. TBD.
class Const(Expression):
    def __init__(self, line, value, type):
        super().__init__(line)
        self.value = value
        self.token_type = type
        self.type = type.replace('V', 'T')
        
    def gen_impl(self, ctx: ParseContext):
        # Guardar en memoria de constantes
        return ctx.func_dir.new_temp(self.type, self.value)

class Id(Expression):
    def __init__(self, line, id):
        super().__init__(line)
        self.id = id
  
    def gen_impl(self, ctx: ParseContext):
        return ctx.func_dir.get_var(self.id)

class Access(Expression):
    def __init__(self, line, id_access, expr):
        super().__init__(line)
        self.id_access = id_access
        self.expr = expr
    
    @property
    def id(self):
        return self.id_access.id

    def gen_impl(self, ctx: ParseContext):
        # use id's access func to get address
        pass

class UnExpr(Expression):
    def __init__(self, line, op, right):
        super().__init__(line)
        self.op = op
        self.right = right

    def gen_impl(self, ctx: ParseContext):
        right_var = self.right.gen(ctx)
        op_name = symbol_to_token[self.op]
        new_type = ctx.semantic_cube.get_type(op_name, right_var.type)
        new_var = ctx.func_dir.new_temp(new_type)
        ctx.add_quadruple(Quadruple(op_name, right_var.mem_dir, None, new_var.name))
        return new_var
