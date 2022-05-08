from abc import ABC, abstractmethod

class Node(ABC):
  def __init__(self, name):
    self.name = name

  @abstractmethod
  def gen():
    pass