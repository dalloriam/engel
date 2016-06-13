from .base import BaseElement
from ..client.compiler.compiler import generate_websocket_handler


class Button(BaseElement):

  def __init__(self, id, text, classname=None, parent=None):
    super(Button, self).__init__(id, classname, parent)
    self.html_tag = "button"

    self.content = text


class TextBox(BaseElement):

  def __init__(self, id, name=None, classname=None, parent=None):
    super(TextBox, self).__init__(id, classname, parent)
    self.html_tag = "input"

    self.text = ""

    self.attributes["type"] = "text"

    if name:
      self.attributes["name"] = name

    self.server_events.append(generate_websocket_handler("change", id, 'function(){{return document.getElementById("{ID}").value;}}'.format(ID=id)))
    self.socket_events["change"] = {id: self._set_text}

  def _set_text(self, text=None):
    if not text:
      self.text = ""
    else:
      self.text = text
