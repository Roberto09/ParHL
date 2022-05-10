from lexer_parser.ast_classes.Node import Node

class Bool(Node):
  def __init__(self, value):
      super().__init__('Bool')
      self.value = value