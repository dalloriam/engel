from .base import BaseContainer
from .abstract import HeadLink


class Document(BaseContainer):
  """
  A document. Analogous to the HTML ``<html>`` element.
  """

  html_tag = "html"

  def __init__(self, id, view, classname=None, parent=None):
    """
    :param view: :class:`~.application.View` in which the document is declared.
    """
    super(Document, self).__init__(id, classname, parent)
    self.view = view


class Head(BaseContainer):
  html_tag = "head"

  def load_script(self, id, path):
    """
    Proper way to dynamically inject a script in a page.

    :param path: Path of the script to inject.
    """
    self.view.dispatch({'name': 'script', 'path': path})

  def load_stylesheet(self, id, path):
    """
    Proper way to dynamically inject a stylesheet in a page.

    :param path: Path of the stylesheet to inject.
    """
    self.add_child(HeadLink(id=id, link_type="stylesheet", path=path))


class Body(BaseContainer):
  """
  Simple container analogous to the html ``<body>`` element.
  """
  html_tag = "body"


class Panel(BaseContainer):

  """
  Simple container analogous to the html ``<div>`` element.
  """

  html_tag = "div"


class List(BaseContainer):

  """
  Bridges python and HTML lists. :class:`List` exposes an interface similar to
  python lists and takes care of updating the corresponding HTML ``<ul>`` when the python object is updated.
  """

  html_tag = "ul"

  def __init__(self, id, classname=None, parent=None):
    super(List, self).__init__(id, classname, parent)
    self._count = 0
    self._items = []

  def append(self, widget):
    """
    Append a widget to the list.

    :param widget: Object inheriting :class:`~.widgets.base.BaseElement`
    """
    li_itm = _li(id=self.attributes["id"] + str(self._count))
    li_itm.add_child(widget)

    self.add_child(li_itm)
    self._items.append((widget, li_itm))
    self._count += 1

  def remove(self, widget):
    """
    Remove a widget from the list.

    :param widget: Object inheriting :class:`~.widgets.base.BaseElement`
    """
    raw = list(filter(lambda x: x[0] == widget, self._items))
    if raw:
      itm, wrapped = raw[0]
      self._items.remove(raw[0])
      self.remove_child(wrapped)
    else:
      raise ValueError("Child not in list.")

  def __len__(self):
    return len(self._items)

  def __getitem__(self, index):
    return self._items[index][0]

  def __setitem__(self, index, widget):
    li_itm = _li(id=self.attributes["id"] + str(self._count))
    # TODO: This manually sets the view since the view is normally set by BaseContainer.add_child()
    # Should investigate overriding the setters on the BaseContainer.children list instead.
    li_itm.view = self.view
    li_itm.add_child(widget)

    self.children[index] = li_itm
    self._items[index] = (widget, li_itm)


class _li(BaseContainer):
  html_tag = "li"
