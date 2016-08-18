from .base import BaseElement


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
    self.content = text
    self.size = size

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
    self.url = url
    super(TextLink, self).__init__(id, classname, parent)

    self.content = text

  def _build(self):
    self.attributes["href"] = self.url
