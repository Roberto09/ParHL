from abc import ABC, abstractmethod
from ..var_dir import FuncDir
class Node(ABC):
    FUNC_DIR = FuncDir()
    @abstractmethod
    def gen(self):
        pass