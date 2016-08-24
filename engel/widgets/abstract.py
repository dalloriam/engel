"""
.. note::
  All widgets in this package are not meant to be used directly. They are mostly used by the framework, or subclassed
  into usable widgets.
"""

from .base import BaseElement

from ..utils import html_property


class HeadLink(BaseElement):
  """
  Widget representing links described in the ``<head>`` section of a typical HTML document.
  This widget is used by the framework to generate links to stylesheets and auto-generated javascript files.
  """

  html_tag = "link"

  target = html_property('href')
  """
  File to which the HeadLink is pointing
  """

  link_type = html_property('rel')
  """
  Link type (Ex: stylesheet)
  """

  def build(self, link_type, path):
    super(HeadLink, self).build()
    """
    :param link_type: Link type
    :param target: Link target
    """
    self.target = path
    self.link_type = link_type
    self.autoclosing = True


class PageTitle(BaseElement):
  """
  Widget representing the title of the page.
  This widget is used by :meth:`~.application.View.render`.
  """

  html_tag = "title"

  def build(self, text):
    super(PageTitle, self).build()
    """
    :param text: Page title
    """
    self.content = text


class Script(BaseElement):
  """
  Widget representing a script element.
  """

  html_tag = "script"

  source = html_property('src')
  """
  Location of the script
  """

  def build(self, js_path):
    super(Script, self).build()
    """
    :param js_path: Javascript source code.
    """
    self.source = js_path
