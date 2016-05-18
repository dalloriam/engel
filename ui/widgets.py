from ui.base import BaseElement


class Button(BaseElement):
  def __init__(self, id=None, classname=None):
    super(Button, self).__init__(id, classname)

  def _get_html_tag(self):
    return "button"
