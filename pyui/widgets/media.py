from .base import BaseElement, BaseContainer
from .abstract import ViewLink


class Image(BaseElement):

  def __init__(self, id, img_url, classname=None):
    super(Image, self).__init__(id, classname)
    self.html_tag = "img"

    self.attributes["src"] = img_url


class ImageLink(BaseContainer):

  def __init__(self, id, link, img_url, classname=None):
    super(ImageLink, self).__init__(id, classname)
    self.html_tag = "a"

    self.attributes["href"] = link

    self.add_child(Image(id, img_url))


class Audio(BaseElement):

  def __init__(self, id, audio_path, classname=None):
    super(Audio, self).__init__(id, classname)
    self.attributes["src"] = audio_path
    self.html_tag = "audio"


class ViewImageLink(ViewLink):

  def __init__(self, id, img_url, view_name, params=None, classname=None):
    super(ViewImageLink, self).__init__(view_name, view_name, params)
    self.add_child(Image(id, img_url, classname=classname))
