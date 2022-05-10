from ast_classes.Node import Node

class Id(Node):
  def __init__(self, id):
      super().__init__('Id')
      self.id = id
  
  def gen(self):
      pass