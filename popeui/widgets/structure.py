from .base import BaseContainer


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
    li_itm = _li(id=self.attributes["id"] + str(self._count), parent=self)
    li_itm.add_child(widget)
    self._items.append((widget, li_itm))
    self._count += 1
    if self.view is not None:
      self.redraw()

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

      # Only send the call to redraw() if the element exists in a rendered view
      if self.view is not None:
        self.redraw()
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

    self.children[index] = li_itm
    self._items[index] = (widget, li_itm)


class _li(BaseContainer):
  html_tag = "li"
