from .semantic_cube import SemanticCube
from .var_dir import FuncDir

class ParseContext():
    def __init__(self):
        self.func_dir = FuncDir()
        self.semantic_cube = SemanticCube()