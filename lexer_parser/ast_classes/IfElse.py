from ast_classes.Node import Node

class IfElse(Node):
    def __init__(self, ifNode, elseNode):
      super().__init__('IfElse')
      self.ifNode = ifNode
      self.elseNode = elseNode
  
    def gen(self):
        self.ifNode.gen()
        self.elseNode.gen()
