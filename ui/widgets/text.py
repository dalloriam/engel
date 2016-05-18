from base import BaseElement


class Title(BaseElement):

  def __init__(self, text, id=None, classname=None, size=1):
    super(Title, self).__init__(id, classname)
    self.size = size
    self.content = text

  def _get_html_tag(self):
    return "h{0}".format(self.size)


class Paragraph(BaseElement):

  def __init__(self, text, id=None, classname=None):
    super(Paragraph, self).__init__(id, classname)
    self.content = text
    self.html_tag = "p"


class TextLink(BaseElement):

  def __init__(self, url, text, id=None, classname=None):
    super(TextLink, self).__init__(id, classname)
    self.html_tag = "a"

    self.content = text
    self.attributes["href"] = url


class ViewTextLink(BaseElement):

  def __init__(self, view, text, id=None, classname=None):
    super(ViewTextLink, self).__init__(id, classname)
    self.html_tag = "a"

    self.content = text
    self.attributes["href"] = view + ".html"
