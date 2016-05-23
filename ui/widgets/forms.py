from .base import BaseElement


class Button(BaseElement):

  def __init__(self, id, text, classname=None):
    super(Button, self).__init__(id, classname)
    self.html_tag = "button"

    self.content = text
