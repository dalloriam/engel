from base import BaseElement, BaseContainer
from abstract import ViewLink


class Image(BaseElement):

  def __init__(self, img_url, id=None, classname=None):
    super(Image, self).__init__(id, classname)
    self.html_tag = "img"

    self.attributes["src"] = img_url


class ImageLink(BaseContainer):

  def __init__(self, link, img_url, id=None, classname=None):
    super(ImageLink, self).__init__(id, classname)
    self.html_tag = "a"

    self.attributes["href"] = link

    self.add_child(Image(img_url))


class ViewImageLink(ViewLink):

  def __init__(self, img_url, view_name, params=None, id=None, classname=None):
    super(ViewImageLink, self).__init__(view_name, params, id, classname)
    self.add_child(Image(img_url))
