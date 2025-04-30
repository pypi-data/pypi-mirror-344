from ..routing import Router

class ServiceLocator:
  _services: dict[str, object] = {}

  @classmethod
  def provide(cls, name: str, service: object):
    cls._services[name] = service

  @classmethod
  def get(cls, name: str) -> Router:
    if name not in cls._services:
      raise Exception(f"Service '{name}' not found.")
    return cls._services[name]

  @classmethod
  def clear(cls):
    cls._services.clear()