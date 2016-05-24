from .base import BaseContainer


class Document(BaseContainer):

  def __init__(self, id, classname=None):
    super(Document, self).__init__(id, classname)
    self.html_tag = "html"


class Head(BaseContainer):

  def __init__(self, id, classname=None):
    super(Head, self).__init__(id, classname)
    self.html_tag = "head"


class Body(BaseContainer):

  def __init__(self, id, classname=None):
    super(Body, self).__init__(id, classname)
    self.html_tag = "body"


class Panel(BaseContainer):

  def __init__(self, id, classname=None):
    super(Panel, self).__init__(id, classname)
    self.html_tag = "div"


class List(BaseContainer):

  def __init__(self, id, classname=None):
    super(List, self).__init__(id, classname)
    self.html_tag = "ul"

  def append(self, html_item):
    self.add_child(_li(html_item))


class _li(BaseContainer):

  def __init__(self, id, item, classname=None):
    super(_li, self).__init__(id, classname)
    self.html_tag = "li"
    self.add_child(item)
