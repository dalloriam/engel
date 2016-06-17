from .base import BaseContainer


class Document(BaseContainer):

  def __init__(self, id, classname=None, parent=None):
    super(Document, self).__init__(id, classname, parent)
    self.html_tag = "html"


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

  def append(self, html_item):
    self.add_child(_li(id=self.attributes["id"] + str(self._count), item=html_item))
    self._count += 1


class _li(BaseContainer):

  def __init__(self, id, item, classname=None, parent=None):
    super(_li, self).__init__(id, classname, parent)
    self.html_tag = "li"
    self.add_child(item)
