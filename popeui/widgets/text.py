from .base import BaseElement
from .abstract import ViewLink


class Title(BaseElement):
  """
  Title widget analogous to the HTML <h{n}> elements.
  """

  def __init__(self, id, text, classname=None, parent=None, size=1):
    """
    :param text: Text of the widget
    :param size: Size of the text (Higher size = smaller title)
    """
    super(Title, self).__init__(id, classname, parent)
    self.size = size
    self.content = text

  def _get_html_tag(self):
    return "h{0}".format(self.size)


class Paragraph(BaseElement):
  """
  Simple paragraph widget
  """

  html_tag = "p"

  def __init__(self, id, text, classname=None, parent=None):
    """
    :param text: Content of the paragraph
    """
    super(Paragraph, self).__init__(id, classname, parent)
    self.content = text


class Span(BaseElement):
  """
  Simple span widget
  """

  html_tag = "span"

  def __init__(self, id, text, classname=None, parent=None):
    """
    :param text: Content of the span
    """
    super(Span, self).__init__(id, classname, parent)
    self.content = text


class TextLink(BaseElement):
  """
  Text widget linking to an external URL.
  """

  html_tag = "a"

  def __init__(self, id, text, url, classname=None, parent=None):
    """
    :param text: Text of the link
    :param url: Target URL
    """
    super(TextLink, self).__init__(id, classname, parent)

    self.content = text
    self.attributes["href"] = url


class ViewTextLink(ViewLink):
  """
  Text widget linking to another view.
  """

  def __init__(self, id, text, view_name, params=None, classname=None, parent=None):
    super(ViewTextLink, self).__init__(id=id, view_name=view_name, params=params, classname=classname, parent=parent)
    self.add_child(Span(id=id + "-span", text=text))
