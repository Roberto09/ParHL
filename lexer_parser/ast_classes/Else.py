from ast_classes.Node import Node

class Else(Node):
    def __init__(self, block):
      super().__init__('Else')
      self.block = block
  
    def gen(self):
        # q = quadruple (goto, None)
        self.block.gen()
        # q.fillJump()
