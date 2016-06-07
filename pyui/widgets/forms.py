from .base import BaseElement


class Button(BaseElement):

  def __init__(self, id, text, classname=None, parent=None):
    super(Button, self).__init__(id, classname, parent)
    self.html_tag = "button"

    self.content = text
