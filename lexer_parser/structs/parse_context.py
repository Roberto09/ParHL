from .semantic_cube import SemanticCube
from .var_dir import FuncDir
from .quadruples import Quadruple
    
class ParseContext():
    def __init__(self):
        self.func_dir = FuncDir()
        self.semantic_cube = SemanticCube()
        self._quadruples: list[Quadruple] = []

    def get_quadruples(self):
        return self._quadruples
    
    def add_quadruple(self, quadruple: Quadruple):
        self._quadruples.append(quadruple)
        return len(self._quadruples)-1
    
    def set_goto_position(self, index):
        self._quadruples[index].result = len(self._quadruples)