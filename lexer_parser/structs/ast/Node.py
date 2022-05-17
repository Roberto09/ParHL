from abc import ABC, abstractmethod

class Node(ABC):
    @abstractmethod
    def gen(self, context):
        pass