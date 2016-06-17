from .base import BaseElement, BaseContainer
from .abstract import ViewLink


class Image(BaseElement):

  def __init__(self, id, img_url, classname=None, parent=None):
    super(Image, self).__init__(id, classname, parent)
    self.html_tag = "img"

    self.attributes["src"] = img_url


class Video(BaseElement):

  def __init__(self, id, vid_url, classname=None, parent=None):
    super(Video, self).__init__(id, classname, parent)
    self.html_tag = "video"

    self.attributes["src"] = vid_url
    self.attributes["loop"] = "true"


class ImageLink(BaseContainer):

  def __init__(self, id, link, img_url, classname=None, parent=None):
    super(ImageLink, self).__init__(id, classname, parent)
    self.html_tag = "a"

    self.attributes["href"] = link

    self.add_child(Image(id, img_url))


class Audio(BaseElement):

  def __init__(self, id, audio_path, classname=None, parent=None):
    super(Audio, self).__init__(id, classname, parent)
    self.attributes["src"] = audio_path
    self.html_tag = "audio"


class ViewImageLink(ViewLink):

  def __init__(self, id, img_url, view_name, params=None, classname=None, parent=None):
    super(ViewImageLink, self).__init__(id=view_name, view_name=view_name, params=params, parent=parent)
    self.add_child(Image(id, img_url, classname=classname))


class ViewVideoLink(ViewLink):

  def __init__(self, id, vid_url, view_name, params=None, classname=None, parent=None):
    super(ViewVideoLink, self).__init__(id=view_name, view_name=view_name, params=params, parent=parent)
    self.add_child(Video(id, vid_url, classname=classname))
