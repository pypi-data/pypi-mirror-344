from abc import ABC, abstractmethod

class BaseNode:
  def __init__(self, path: str, screen: object, name: str):
    
    if not isinstance(path, str):
      raise TypeError("Route path should string.")
    
    if not path.startswith('/'):
      raise SyntaxError("Route path should start with '/'.")
    
    if not isinstance(screen, object):
      raise TypeError("Screen should be QtWidgets object.")
    

class Expression(ABC):

  @abstractmethod
  def interpret(self, path_segment: str):
    pass

class Literal(Expression):

  def __init__(self, text: str):
    if not isinstance(text, str):
      raise TypeError("Literal text should be string.")
    self.text = text

  def interpret(self, path_segment: str):
    return self.text == path_segment
  
class Variable(Expression):

  def __init__(self, name: str):
    if not isinstance(name, str):
      raise TypeError("Variable name should be string.")
    self.name = name

  def interpret(self, path_segment: str):
    return True
  
  def extract_value(self, path_segment: str):
    return path_segment