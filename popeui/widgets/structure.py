from .base import BaseContainer


class Document(BaseContainer):

  def __init__(self, id, view, classname=None, parent=None):
    super(Document, self).__init__(id, classname, parent)
    self.html_tag = "html"
    self.view = view


class Head(BaseContainer):

  def __init__(self, id, classname=None, parent=None):
    super(Head, self).__init__(id, classname, parent)
    self.html_tag = "head"


class Body(BaseContainer):

  def __init__(self, id, classname=None, parent=None):
    super(Body, self).__init__(id, classname, parent)
    self.html_tag = "body"


class Panel(BaseContainer):

  def __init__(self, id, classname=None, parent=None):
    super(Panel, self).__init__(id, classname, parent)
    self.html_tag = "div"


class List(BaseContainer):

  def __init__(self, id, classname=None, parent=None):
    super(List, self).__init__(id, classname, parent)
    self.html_tag = "ul"
    self._count = 0
    self._items = []

  def append(self, html_item):
    li_itm = _li(id=self.attributes["id"] + str(self._count), parent=self)
    li_itm.add_child(html_item)
    self._items.append((html_item, li_itm))
    self._count += 1
    if self.view is not None:
      self.redraw()

  def remove(self, html_item):
    raw = list(filter(lambda x: x[0] == html_item, self._items))
    if raw:
      itm, wrapped = raw[0]
      self._items.remove(raw[0])
      self.remove_child(wrapped)
      self._count -= 1

      # Only send the call to redraw() if the element exists in a rendered view
      if self.view is not None:
        self.redraw()
    else:
      raise ValueError("Child not in list.")

  def __getitem__(self, index):
    return self._items[index][0]

  # TODO: Add __setitem__()


class _li(BaseContainer):

  def __init__(self, id, classname=None, parent=None):
    super(_li, self).__init__(id, classname, parent)
    self.html_tag = "li"
