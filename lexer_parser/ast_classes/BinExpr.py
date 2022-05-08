from lexer_parser.ast_classes.Node import Node

class BinExpr(Node):
  def __init__(self, left, op, right):
    super().__init__('BinExpr')
    self.left = left
    self.right = right
    self.op = op

  def gen():
    left.gen()
    if hasattr(self, 'right'):
      right.gen()
      # newType = SemanticCube.get_type(op, left, right)
      # malloc temp : newType
      # quadruple('OR', left, right, temp)