from base import BaseElement


class Image(BaseElement):

  def __init__(self, img_url, id=None, classname=None):
    super(Image, self).__init__(id, classname)
    self.html_tag = "img"

    self.attributes["src"] = img_url
