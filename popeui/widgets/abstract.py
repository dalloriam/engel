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

  path = html_property('href')
  link_type = html_property('rel')

  def __init__(self, id, link_type, path, classname=None, parent=None):
    """
    :param link_type: Type of link (Ex: "stylesheet", "script")
    :param path: Path of the link's target
    """
    super(HeadLink, self).__init__(id, classname, parent)
    self.path = path
    self.link_type = link_type
    self.autoclosing = True


class PageTitle(BaseElement):
  """
  Widget representing the title of the page.
  This widget is used by :meth:`~.application.View.render`.
  """

  html_tag = "title"

  def __init__(self, id, text, classname=None, parent=None):
    """
    :param text: Title of the page.
    """
    super(PageTitle, self).__init__(id, classname, parent)
    self.content = text


class Script(BaseElement):
  """
  Widget representing a script element.
  """

  html_tag = "script"

  source = html_property('src')

  def __init__(self, id, js_path, classname=None, parent=None):
    """
    :param js_path: Javascript source code.
    """
    super(Script, self).__init__(id, classname, parent)
    self.source = js_path
