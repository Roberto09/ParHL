from .Node import Node
from ..parse_context import ParseContext
from ..quadruples import Quadruple

class Expression(Node):
    def __init__(self):
        self._id_type = None

    def id_type(self):
        assert self._id_type is not None
        return self._id_type

    def set_id_type(self, id, type):
        self._id_type = id, type


class Assign(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
  
    def gen(self, ctx: ParseContext):
        left_var = self.right.gen(ctx)
        right_var = self.left.gen(ctx)
        ctx.semantic_cube.get_type('ASSIG',left_var, right_var)
        ctx.add_quadruple(Quadruple('ASSIG', right_var, None, left_var
        ))
        # quadruple('=', exp, None, var)


class BinExpr(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.right = right
        self.op = op

    def gen(self, ctx: ParseContext):
        left_var = self.left.gen(ctx)
        if hasattr(self, 'right'):
            right_var = self.right.gen(ctx)
            new_type = ctx.semantic_cube.get_type(self.op, self.right)
            temp_var = ctx.func_dir.new_temp(new_type)
            ctx.add_quadruple(Quadruple(self.op, left_var, right_var, temp_var))
            return temp_var


# This implementation depends a bit on how we actually want to handle
# constants in memory and in quadruples. TBD.
class Const(Expression):
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def gen(self, ctx: ParseContext):
        # Guardar en memoria de constantes
        pass


class Id(Expression):
    def __init__(self, id):
        self.id = id
  
    def gen(self, ctx: ParseContext):
        return ctx.get_var(self.id)

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
        new_type = ctx.semantic_cube.get_type(self.op, self.right)
        new_var = ctx.func_dir.new_temp(new_type)
        ctx.add_quadruple(Quadruple(self.op, right_var, new_var))
        return new_var
        # quadruple(op, arg, None, temp)