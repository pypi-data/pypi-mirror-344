from typing import Dict
from .route import Route
from ..core import SegmentUtils

class RouteMap:

  routeMapByName: Dict[str, Route] = {}
  routeMapByPath: Dict[str, Route] = {}
  segmentMap: Dict[int, list[Route]] = {}

  def __init__(self):
    self.segment = SegmentUtils()

  def register_route(self, route: Route):
    """
    Register a route in the route map.
    """
    if not isinstance(route, Route):
      raise TypeError("Route should be an instance of Route.")
    
    if self.__is_exist(route.node.name, route.node.path):
      raise ValueError(f"Route with name {route.node.name} or path {route.node.path} already exists.")
    
    if route.node.name != None:
      self.routeMapByName[route.node.name] = route
      
    self.routeMapByPath[route.node.path] = route
    self.segment.process_segments(route.node.path)
    
    if self.segment.count not in self.segmentMap.keys():
      self.segmentMap[self.segment.count] = [route]
    else:
      self.segmentMap[self.segment.count].append(route)

  def __is_exist(self, name, path):
    """
    Check if a route exists in the route map.
    """
    if name in self.routeMapByName.keys() or path in self.routeMapByPath.keys():
      return True
    
    return False