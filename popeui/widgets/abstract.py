"""
.. note::
  All widgets in this package are not meant to be used directly. They are mostly used by the framework, or subclassed
  into usable widgets.
"""

from .base import BaseContainer, BaseElement


class ViewLink(BaseContainer):
  """
  Base class for all widgets with the ability of linking to other views.
  """

  html_tag = "a"

  def __init__(self, id, view_name, params=None, classname=None, parent=None):
    """
    :param view_name: Name of the view referenced by this widget
    :param params: Dictionary of parameters to pass to the target view. The parameters will be encoded in the URL.
    """
    super(ViewLink, self).__init__(id, classname, parent)
    url = view_name
    if params:
      query_string = "&".join([str(x) + "=" + str(params[x]) for x in params.keys()])
      if query_string:
        url += "?" + query_string

    self.attributes["href"] = url


class HeadLink(BaseElement):
  """
  Widget representing links described in the ``<head>`` section of a typical HTML document.
  This widget is used by the framework to generate links to stylesheets and auto-generated javascript files.
  """

  html_tag = "link"

  def __init__(self, id, link_type, path, classname=None, parent=None):
    """
    :param link_type: Type of link (Ex: "stylesheet", "script")
    :param path: Path of the link's target
    """
    super(HeadLink, self).__init__(id, classname, parent)
    self.attributes["href"] = path
    self.attributes["rel"] = link_type
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
  This widget is used by :meth:`~.application.View.render` as a host for the sum of all the compiled client methods.
  """

  html_tag = "script"

  def __init__(self, id, js, classname=None, parent=None):
    """
    :param js: Javascript source code.
    """
    super(Script, self).__init__(id, classname, parent)
    self.content = js
