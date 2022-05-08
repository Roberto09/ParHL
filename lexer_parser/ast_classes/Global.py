from lexer_parser.ast_classes.Node import Node

class Global(Node):
  def __init__(self, estatuto, global_1):
    super().__init__('Global')
    self.estatuto = estatuto
    self.global_1 = global_1
  
  def gen():
    self.estatuto.gen()
    if(self.global_1):
      self.global_1.gen()