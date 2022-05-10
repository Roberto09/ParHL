from lexer_parser.ast_classes.Node import Node

class String(Node):
  def __init__(self, value):
      super().__init__('String')
      self.value = value