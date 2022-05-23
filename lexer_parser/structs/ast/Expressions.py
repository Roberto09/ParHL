from ast import Expression
from .Node import Node
from ..parse_context import ParseContext
from ..quadruples import Quadruple
from ...lexer import symbol_to_token

Expression = Node

class Assign(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
  
    def gen(self, ctx: ParseContext):
        right_var = self.right.gen(ctx)
        left_var = self.left.gen(ctx)
        ctx.semantic_cube.get_type('ASSIG',left_var.type, right_var.type)
        ctx.add_quadruple(Quadruple('ASSIG', right_var.name, None, left_var.name))


class BinExpr(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.right = right
        self.op = op

    def gen(self, ctx: ParseContext):
        left_var = self.left.gen(ctx)
        right_var = self.right.gen(ctx)
        op_name = symbol_to_token[self.op]
        new_type = ctx.semantic_cube.get_type(op_name, left_var.type, right_var.type)
        temp_var = ctx.func_dir.new_temp(new_type)
        # Need to change names to mem_dirs when they are functioning
        ctx.add_quadruple(Quadruple(op_name, left_var.name, right_var.name, temp_var.name))
        return temp_var


# This implementation depends a bit on how we actually want to handle
# constants in memory and in quadruples. TBD.
class Const(Expression):
    def __init__(self, value, type):
        self.value = value
        self.token_type = type
        self.type = type.replace('V', 'T')
        
    def gen(self, ctx: ParseContext):
        # Guardar en memoria de constantes
        return ctx.func_dir.new_temp(self.type, self.value)

class Id(Expression):
    def __init__(self, id):
        self.id = id
  
    def gen(self, ctx: ParseContext):
        return ctx.func_dir.get_var(self.id)

class Access(Expression):
    def __init__(self, id_access, expr):
        self.id_access = id_access
        self.expr = expr
    
    @property
    def id(self):
        return self.id_access.id

    def gen(self, ctx: ParseContext):
        # use id's access func to get address
        pass

class UnExpr(Expression):
    def __init__(self, op, right):
        self.op = op
        self.right = right

    def gen(self, ctx: ParseContext):
        right_var = self.right.gen(ctx)
        op_name = symbol_to_token[self.op]
        new_type = ctx.semantic_cube.get_type(op_name, right_var.type)
        new_var = ctx.func_dir.new_temp(new_type)
        ctx.add_quadruple(Quadruple(op_name, right_var.name, None, new_var.name))
        return new_var
