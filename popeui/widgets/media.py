from .base import BaseElement, BaseContainer
from .abstract import ViewLink


class Image(BaseElement):
  """
  A simple image widget.
  """

  html_tag = "img"

  def __init__(self, id, img_url, classname=None, parent=None):
    super(Image, self).__init__(id, classname, parent)
    self.attributes["src"] = img_url


class Video(BaseElement):
  """
  A simple video widget, set via ``Video.attributes`` to loop by default.
  """

  html_tag = "video"

  def __init__(self, id, vid_url, classname=None, parent=None):
    super(Video, self).__init__(id, classname, parent)
    self.attributes["src"] = vid_url
    self.attributes["loop"] = "true"


class ImageLink(BaseContainer):
  """
  An image widget, with the added feature of linking to an external URL.
  """

  html_tag = "a"

  def __init__(self, id, link, img_url, classname=None, parent=None):
    super(ImageLink, self).__init__(id, classname, parent)
    self.attributes["href"] = link

    self.add_child(Image(id, img_url))


class Audio(BaseElement):
  """
  A simple audio widget.
  """

  html_tag = "audio"

  def __init__(self, id, audio_path, classname=None, parent=None):
    super(Audio, self).__init__(id, classname, parent)
    self.attributes["src"] = audio_path


class ViewImageLink(ViewLink):
  """
  An image widget, with the added feature of linking to another view
  """

  def __init__(self, id, img_url, view_name, params=None, classname=None, parent=None):
    super(ViewImageLink, self).__init__(id=view_name, view_name=view_name, params=params, parent=parent)
    self.add_child(Image(id, img_url, classname=classname))


class ViewVideoLink(ViewLink):
  """
  A video widget, with the added feature of linking to another view.
  """

  def __init__(self, id, vid_url, view_name, params=None, classname=None, parent=None):
    super(ViewVideoLink, self).__init__(id=view_name, view_name=view_name, params=params, parent=parent)
    self.add_child(Video(id, vid_url, classname=classname))
