from .base import BaseElement

from ..utils import html_property


class Title(BaseElement):
  """
  Title widget analogous to the HTML <h{n}> elements.
  """

  def build(self, text, size=1):
    """
    :param text: Text of the widget
    :param size: Size of the text (Higher size = smaller title)
    """
    super(Title, self).build()
    self.content = text
    self.size = size

  def _get_html_tag(self):
    return "h{0}".format(self.size)


class Paragraph(BaseElement):
  """
  Simple paragraph widget
  """

  html_tag = "p"

  def build(self, text):
    """
    :param text: Content of the paragraph
    """
    super(Paragraph, self).build()
    self.content = text


class Span(BaseElement):
  """
  Simple span widget
  """

  html_tag = "span"

  def build(self, text):
    """
    :param text: Content of the span
    """
    super(Span, self).build()
    self.content = text


class TextLink(BaseElement):
  """
  Text widget linking to an external URL.
  """

  html_tag = "a"

  target = html_property('href')
  """
  Target of the link
  """

  def build(self, text, url):
    """
    :param text: Text of the link
    :param url: Target URL
    """
    super(TextLink, self).build()
    self.target = url
    self.content = text
