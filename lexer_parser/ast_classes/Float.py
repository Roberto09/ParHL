from lexer_parser.ast_classes.Node import Node

class Float(Node):
  def __init__(self, value):
      super().__init__('Float')
      self.value = value