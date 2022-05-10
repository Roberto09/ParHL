from Node import Node

class Assign(Node):
  def __init__(self, id, expr):
    super().__init__('Assing')
    self.id = id
    self.expr = expr
  
  def gen(self):
    self.expr.gen()
    # var = FuncDir.getVar(id)
    # exp = FuncDor.getVar(exp)
    # Check expr can be assigned to var
    # SemanticCube.get_type('ASSIG', var.type, exp.type)

    # quadruple('=', exp, None, var)


class BinExpr(Node):
  def __init__(self, left, op, right):
    super().__init__('BinExpr')
    self.left = left
    self.right = right
    self.op = op

  def gen(self):
    self.left.gen()
    if hasattr(self, 'right'):
      self.right.gen()
      # newType = SemanticCube.get_type(op, left, right)
      # malloc temp : newType
      # quadruple(op, left, right, temp)


class Const(Node):
  def __init__(self, value, type):
      super().__init__('Const')
      self.value = value
      self.type = type

  def gen(self):
    # Guardar en memoria de constantes
    pass


class Id(Node):
  def __init__(self, id):
      super().__init__('Id')
      self.id = id
  
  def gen(self):
      pass


class UnExpr(Node):
  def __init__(self, op, arg):
    super().__init__('UnExpr')
    self.op = op
    self.arg = arg

  def gen(self):
    self.arg.gen()
    # newType = SC.get_type(op, arg)
    # malloc temp : newType
    # quadruple(op, arg, None, temp)