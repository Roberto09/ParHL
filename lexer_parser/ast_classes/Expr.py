from lexer_parser.ast_classes.Node import Node

class Expr(Node):
  def __init__(self, left, right):
    super().__init__('Expr')
    self.left = left
    self.right = right

  def gen():
    left.gen()
    if hasattr(self, 'right'):
      right.gen()
      # newType = SemanticCube.get_type('OR', left, right)
      # malloc temp : newType
      # quadruple('OR', left, right, temp)