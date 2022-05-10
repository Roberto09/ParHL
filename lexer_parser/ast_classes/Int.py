from lexer_parser.ast_classes.Node import Node

class Int(Node):
  def __init__(self, value) -> None:
      super().__init__('Int')
      self.value = value