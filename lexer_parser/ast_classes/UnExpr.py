from ast_classes.Node import Node

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