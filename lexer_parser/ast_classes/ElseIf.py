from ast_classes.Node import Node

class ElseIf(Node):
    def __init__(self, expr, block, nextElseIf):
      super().__init__('ElseIf')
      self.expr = expr
      self.block = block
      self.nextElseIf = nextElseIf
  
    def gen(self):
        # q = quadruple (goto, None)
        self.expr.gen()
        # qIf = quadruple (gotoF, lastTemp, , None)
        self.block.gen()
        # q.fillJump()
        # qIf.fillJump()
        if hasattr(self, 'nextElseIf'):
            self.nextElseIf.gen()
