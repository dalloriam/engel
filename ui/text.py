from base import BaseElement


class Title(BaseElement):

  def __init__(self, id=None, classname=None, size=1):
    super(Title, self).__init__(id, classname)
    self.size = size

  def _get_html_tag(self):
    return "h{0}".format(self.size)


class Span(BaseElement):

  def __init__(self, id=None, classname=None):
    super(Span, self).__init__(id, classname)

  def _get_html_tag(self):
    return "span"
