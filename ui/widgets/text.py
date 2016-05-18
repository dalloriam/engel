from base import BaseElement
from abstract import ViewLink


class Title(BaseElement):

  def __init__(self, text, id=None, classname=None, size=1):
    super(Title, self).__init__(id, classname)
    self.size = size
    self.content = text

  def _get_html_tag(self):
    return "h{0}".format(self.size)


class Paragraph(BaseElement):

  def __init__(self, text, id=None, classname=None):
    super(Paragraph, self).__init__(id, classname)
    self.content = text
    self.html_tag = "p"


class Span(BaseElement):

  def __init__(self, text, id=None, classname=None):
    super(Span, self).__init(id, classname)
    self.content = text
    self.html_tag = "span"


class TextLink(BaseElement):

  def __init__(self, text, url, id=None, classname=None):
    super(TextLink, self).__init__(id, classname)
    self.html_tag = "a"

    self.content = text
    self.attributes["href"] = url


class ViewTextLink(ViewLink):

  def __init__(self, text, view_name, params=None, id=None, classname=None):
    super(ViewTextLink, self).__init__(view_name, params, id, classname)
    self.add_child(Span(text=text))
