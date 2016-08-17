import html

from .base import BaseElement


class Button(BaseElement):
  """
  A simple button.
  """

  html_tag = "button"

  def __init__(self, id, text, classname=None, parent=None):
    super(Button, self).__init__(id, classname, parent)
    self.content = text


class TextBox(BaseElement):
  """
  A simple textbox.

  **Default Events**:

  ``OnChange`` (client-side)
    Updates the python object to match the client textbox value.
  """

  html_tag = 'input'

  def __init__(self, id, name=None, classname=None, parent=None):
    self.name = name
    super(TextBox, self).__init__(id, classname, parent)

  def _build(self):
    self.text = ""
    """
    Contents of the textbox.
    """

    self.attributes["type"] = "text"

    if self.name:
      self.attributes["name"] = self.name

  def _set_text(self, event, interface):
    self.text = event['event_object']['target']['value']

  def __setattr__(self, name, value):
    super(TextBox, self).__setattr__(name, value)
    if name == 'view' and value is not None:
      self.view.on('change', self._set_text, '#' + str(self.attributes['id']))

    elif name == 'text' and value:
      self.__dict__[name] = html.escape(value)
