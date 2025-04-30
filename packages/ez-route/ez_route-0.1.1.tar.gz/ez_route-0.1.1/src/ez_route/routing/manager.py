from .route import Route
from .route_interpreter import RouteInterpreter
from .registry import RouteMap
from ..core import SegmentUtils

class RouteManager:

  def __init__(self, route_map: RouteMap):
    self.route_map = route_map
    self.segments = SegmentUtils()

  def get_route_by_name(self, name: str) -> Route:
    """
    Get a route by its name.
    """
    return self.route_map.routeMapByName.get(name, False)
  
  def get_route_by_path(self, path: str) -> tuple[Route, dict]:
    """
    Get a route by its path.
    """
    get_route = self.route_map.routeMapByPath.get(path, False)

    if not get_route:
      self.segments.process_segments(path)
      if self.segments.count in self.route_map.segmentMap.keys():
        for route in self.route_map.segmentMap[self.segments.count]:
          route_interpreter = RouteInterpreter(route, path)
          if route_interpreter.interpret():
            params = route_interpreter.extract_params()
            return route, params
          
      return "Route not found."
     
    return get_route, {}