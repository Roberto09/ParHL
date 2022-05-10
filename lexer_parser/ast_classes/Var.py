from lexer_parser.ast_classes.Node import Node
from lexer_parser.ast_classes.Assign import Assign

class Var(Node):
  def __init__(self, id, id_type, expr):
    super().__init__('Var')
    self.id = id
    self.id_type = id_type
    self.expr = expr

  def gen(self):
    #  FuncDir.add_var(id, id_type)
    if hasattr(self, 'expr'):
      self.expr.gen()
      assign = Assign(id, self.expr)
      assign.gen()