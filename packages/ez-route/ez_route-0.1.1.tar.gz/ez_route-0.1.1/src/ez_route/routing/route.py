from ..core import BaseNode, Expression, Literal, Variable
from ..core import SegmentUtils
from ..platform import QtScreenFactory, TkScreenFactory
from PySide6.QtWidgets import QMainWindow
from tkinter import Frame
from PySide6.QtWidgets import QWidget
    
class RouteNode(BaseNode):
  def __init__(self, path, screen, name):
    super().__init__(path, screen, name)
    self.path = path
    self.screen: Frame | QWidget = screen
    self.name = name
    self.pattern: list[Expression] = None

  def __repr__(self):
    return self.__class__.__name__

class Route:
  def __init__(self, path: str, screen: object, route_name: str = None):
    
    if not path.startswith("/"):
      raise Exception("Path should start with '/'")
    
    if route_name is None:
      name = self.__split_path(path)[0]
      if name.startswith(":"):
        raise Exception("Route that use parameter need speciific route name.")
      
    if route_name != None and not isinstance(route_name, str):
      raise Exception("Route name must string type.")
    
    self.node = RouteNode(path, screen, route_name)
    self.children = []
    self.patter_process()

  def patter_process(self):
    """
    Process the path to create a pattern for matching using Interpreter Pattern.
    """
    self.node.pattern = []
    for segment in self.__split_path(self.node.path):
      if segment.startswith(":"):
        self.node.pattern.append(Variable(segment[1:]))
      else:
        self.node.pattern.append(Literal(segment))
  
  def add_child_route(self, route: 'Route'):
    """
    Add a child route to the current route.
    """
    if isinstance(route, Route):
      self.__process_child_path(route)
    else:
      raise TypeError("Route should be an instance of Route.")

  def add_children_routes(self, routes: list['Route'] | tuple['Route']):
    """
    Add multiple child routes to the current route.
    """
    if isinstance(routes, list) or isinstance(routes, tuple):
      for route in routes:
        self.add_child_route(route)

  def __process_child_path(self, route: 'Route'):
    route.node.path = '/'.join([*self.__split_path(self.node.path), *self.__split_path(route.node.path)])
    route.node.path = '/' + route.node.path
    route.patter_process()
    self.children.append(route)

  def __split_path(self, path: str):
    """
    Split the path into segments.
    """
    return self.__split_process(path)
  
  def __split_process(self, path: str):
    seg_utils = SegmentUtils()
    seg_utils.process_segments(path)
    return seg_utils.items
  
  def display(self, main_frame: QMainWindow | Frame, **params):
    raise NotImplementedError("Display method is not implemented.")


class QtRoute(Route):

  def __init__(self, path, screen, route_name = None):
    super().__init__(path, screen, route_name)
    self.factory = QtScreenFactory()

  def display(self, main_frame: QMainWindow, **params):
    if not isinstance(main_frame, QMainWindow):
      raise TypeError("QtRoute's main_frame must be QMainWindow.")
    screen = self.factory.create(self.node.screen, **params)
    main_frame.setCentralWidget(screen)
    main_frame.show()

class TkRoute(Route):

  def __init__(self, path, screen, route_name = None):
    super().__init__(path, screen, route_name)
    self.factory = TkScreenFactory()

  def display(self, main_frame: Frame, **params):
    if self.factory.main_frame == None:
      self.factory.set_mainFrame(main_frame)

    if not isinstance(main_frame, Frame):
      raise TypeError("TkRoute's main_frame must be tk.Frame.")
    
    # for child in main_frame.winfo_children():
    #   child.destroy()
    
    screen = self.factory.create(self.node.screen, **params)
    screen.tkraise()