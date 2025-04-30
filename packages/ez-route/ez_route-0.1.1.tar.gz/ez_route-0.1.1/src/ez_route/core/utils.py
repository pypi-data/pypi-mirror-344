class SegmentUtils:

  def __init__(self):
    self.items = []
    self.count = 0
  
  def process_segments(self, path: str):
    """
    Process the segments of the path.
    """
    self.items = [*path.strip("/").split("/")]
    self.count = len(self.items)