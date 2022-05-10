from ast_classes.Node import Node

class Globals(Node):
  def __init__(self, statement, global_1):
    super().__init__('Global')
    self.statement = statement
    self.global_1 = global_1
  
  def gen(self):
    if hasattr(self, 'statement'):
      # Checar self.statement.name != 'Return'
      self.statement.gen()
    if hasattr(self, 'global_1'):
      self.global_1.gen()