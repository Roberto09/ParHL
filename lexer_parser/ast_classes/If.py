from ast_classes.Node import Node

class If(Node):
  def __init__(self, expr, block):
      super().__init__('If')
      self.expr = expr
      self.block = block
  
  def gen(self):
      self.expr.gen()
      # q = quadruple (gotoF, lastTemp, , None)
      self.block.gen()
      # q.fillJump()

