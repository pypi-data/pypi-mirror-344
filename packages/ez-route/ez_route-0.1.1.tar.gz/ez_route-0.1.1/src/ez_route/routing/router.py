from .registry import RouteMap
from .route import Route
from .manager import RouteManager

class Router:

  def __init__(self, main_frame):
    self.main_frame = main_frame
    self.route_map = RouteMap()
    self.manager = RouteManager(self.route_map)

  def install_route(self, route: Route):
    """
    Register a route in the router.
    """
    if not isinstance(route, Route):
      raise TypeError("Route should be an instance of Route.")
    
    if route.node.name in self.route_map.routeMapByName.keys():
      raise ValueError(f"Route with name {route.node.name} already exists.")
    
    if route.node.path in self.route_map.routeMapByPath.keys():
      raise ValueError(f"Route with path {route.node.path} already exists.")
    
    self.route_map.register_route(route)
    
    if len(route.children) > 0:
      for child in route.children:
        self.install_route(child)

  def go_by_name(self, name: str, params = {}) -> object:
    """
    Get a route by its name.
    """
    route = self.manager.get_route_by_name(name)
    route.display(self.main_frame, **params)
  
  def go_by_path(self, path: str) -> Route:
    """
    Get a route by its path.
    """
    route, params = self.manager.get_route_by_path(path)
    route.display(self.main_frame, **params)