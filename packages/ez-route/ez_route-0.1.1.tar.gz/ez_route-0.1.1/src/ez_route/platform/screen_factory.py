from abc import ABC, abstractmethod
from PySide6.QtWidgets import QWidget
from tkinter.ttk import Frame

class BaseScreenFactory(ABC):

  @abstractmethod
  def create(cls, screen: QWidget | Frame, **params):
    pass

class QtScreenFactory(BaseScreenFactory):

  def create(cls, screen: QWidget, **params):
    instance = screen()
    if hasattr(instance, "with_param") and params:
      instance.with_param(**params)
    return instance
  

class TkScreenFactory(BaseScreenFactory):

  main_frame: Frame = None

  def create(cls, screen: Frame, **params) -> Frame:
    instance :Frame = screen(cls.main_frame)
    instance.place(relx=0, rely=0, relheight=1, relwidth=1)
    if hasattr(instance, "with_param") and params:
      instance.with_param(**params)
    return instance
  
  def set_mainFrame(cls, main_frame: Frame):
    cls.main_frame = main_frame