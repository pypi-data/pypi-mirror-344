from ..core.base import Expression, Variable
from ..core.utils import SegmentUtils
from .route import Route

class RouteInterpreter(Expression):
  """
  This class is responsible for interpreting the route from the URL and
  returning the corresponding controller and action.
  """

  def __init__(self, route: Route, path: str):
    if not isinstance(route, Route):
      raise TypeError("Route should be an instance of Route.")
    
    self.node = route.node
    self.path = path
    self.seg_utils = SegmentUtils()
    self.seg_utils.process_segments(self.path)

  def interpret(self):
    zip_segments, segments_count = self.zip_segment()

    if segments_count != len(self.node.pattern):
      return False
    
    for segment, expr in zip_segments:
      if not expr.interpret(segment):
        return False
      
    return True
  
  def extract_params(self):
    zip_segments, _ = self.zip_segment()
    params = {}
    
    for segment, expr in zip_segments:
      if isinstance(expr, Variable):
        params[expr.name] = expr.extract_value(segment)
    
    return params
  
  def zip_segment(self):
    """
    Split the path into segments and zip them with the pattern. Return the zipped segments and the count of segments.
    This is used for matching and extracting parameters from the path.
    """
    return zip(self.seg_utils.items, self.node.pattern), self.seg_utils.count