from .Node import Node

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
  
    def gen(self, ctx):
        self.right.gen(ctx)
        self.left.gen(ctx)
        # var = FuncDir.getVar(id)
        # exp = FuncDor.getVar(exp)
        # Check expr can be assigned to var
        # SemanticCube.get_type('ASSIG', var.type, exp.type)

        # quadruple('=', exp, None, var)


class BinExpr(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.right = right
        self.op = op

    def gen(self, ctx):
        self.left.gen(ctx)
        if hasattr(self, 'right'):
            self.right.gen(ctx)
            # newType = SemanticCube.get_type(op, left, right)
            # malloc temp : newType
            # quadruple(op, left, right, temp)


# This implementation depends a bit on how we actually want to handle
# constants in memory and in quadruples. TBD.
class Const(Expression):
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def gen(self, ctx):
        # Guardar en memoria de constantes
        pass


class Id(Expression):
    def __init__(self, id):
        self.id = id
  
    def gen(self, ctx):
        pass
class Access(Expression):
    def __init__(self, id_access, expr):
        self.id_access = id_access
        self.expr = expr
    
    @property
    def id(self):
        return self.id_access.id

    def gen(self, ctx):
        pass


class UnExpr(Expression):
    def __init__(self, op, right):
        self.op = op
        self.right = right

    def gen(self, ctx):
        self.right.gen(ctx)
        # newType = SC.get_type(op, arg)
        # malloc temp : newType
        # quadruple(op, arg, None, temp)