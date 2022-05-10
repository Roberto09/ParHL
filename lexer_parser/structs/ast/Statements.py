from Node import Node

Statement = Node


class Globals(Node):
  def __init__(self, estatuto, global_1):
    super().__init__('Global')
    self.estatuto = estatuto
    self.global_1 = global_1
  
  def gen(self):
    # Checar self.estatuto.name != 'Return'
    self.estatuto.gen()
    if hasattr(self, 'global_1'):
      self.global_1.gen()

    
class Var(Node):
  def __init__(self, id, id_type, expr):
    super().__init__('Var')
    self.id = id
    self.id_type = id_type
    self.expr = expr

  def gen(self):
    #  FuncDir.add_var(id, id_type)
    if hasattr(self, 'expr'):
      self.expr.gen()
      assign = Assign(id, self.expr)
      assign.gen()