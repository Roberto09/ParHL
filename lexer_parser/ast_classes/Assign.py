from ast_classes.Node import Node

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
    

