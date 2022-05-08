from lexer_parser.ast_classes.Node import Node

class Assign(Node):
  def __init__(self, id, expr):
    super().__init__('Assing')
    self.id = id
    self.expr = expr
  
  def gen():
    # var = FuncDir.getVar(id)
    # exp = FuncDor.getVar(exp)
    # newType = SemanticCube.get_type('ASSIG', var.type, exp.type)
    # malloc temp : newType
    # quadruple('=', exp, None, var)
    print('Gen Assin')

