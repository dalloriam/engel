from .base import BaseElement
from .abstract import ViewLink


class Title(BaseElement):

  def __init__(self, id, text, classname=None, parent=None, size=1):
    super(Title, self).__init__(id, classname, parent)
    self.size = size
    self.content = text

  def _get_html_tag(self):
    return "h{0}".format(self.size)


class Paragraph(BaseElement):

  def __init__(self, id, text, classname=None, parent=None):
    super(Paragraph, self).__init__(id, classname, parent)
    self.content = text
    self.html_tag = "p"


class Span(BaseElement):

  def __init__(self, id, text, classname=None, parent=None):
    super(Span, self).__init__(id, classname, parent)
    self.content = text
    self.html_tag = "span"


class TextLink(BaseElement):

  def __init__(self, id, text, url, classname=None, parent=None):
    super(TextLink, self).__init__(id, classname, parent)
    self.html_tag = "a"

    self.content = text
    self.attributes["href"] = url


class ViewTextLink(ViewLink):

  def __init__(self, id, text, view_name, params=None, classname=None, parent=None):
    super(ViewTextLink, self).__init__(id=id, view_name=view_name, params=params, classname=classname, parent=parent)
    self.add_child(Span(id=id + "-span", text=text))
