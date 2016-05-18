from base import BaseElement


class Button(BaseElement):

  def __init__(self, text, id=None, classname=None):
    super(Button, self).__init__(id, classname)
    self.html_tag = "button"

    self.content = text

  def on_server_click(self, action):
    self.attributes["onclick"] = "pushAction('print_ok')"
