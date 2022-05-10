from ast_classes.Node import Node

class Const(Node):
  def __init__(self, value, type):
      super().__init__('Const')
      self.value = value
      self.type = type

  def gen(self):
    # Guardar en memoria de constantes
    pass