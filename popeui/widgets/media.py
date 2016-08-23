from .base import BaseElement, BaseContainer

from ..utils import html_property


class Image(BaseElement):
  """
  A simple image widget.
  """

  html_tag = "img"

  source = html_property('src')

  def __init__(self, id, img_url, classname=None, parent=None):
    super(Image, self).__init__(id, classname, parent)
    self.source = img_url


class Video(BaseElement):
  """
  A simple video widget, set via ``Video.loop`` to loop by default.
  """

  html_tag = "video"

  source = html_property('src')
  loop = html_property('loop')

  def __init__(self, id, vid_url, classname=None, parent=None):
    super(Video, self).__init__(id, classname, parent)

    self.source = vid_url
    self.loop = 'true'


class ImageLink(BaseContainer):
  """
  An image widget, with the added feature of linking to an external URL.
  """

  html_tag = "a"

  target = html_property('href')

  def __init__(self, id, link, img_url, classname=None, parent=None):
    super(ImageLink, self).__init__(id, classname, parent)
    self.target = link
    self.add_child(Image(self.id + '-img', img_url))


class Audio(BaseElement):
  """
  A simple audio widget.
  """

  html_tag = "audio"

  source = html_property('src')

  def __init__(self, id, audio_path, classname=None, parent=None):
    super(Audio, self).__init__(id, classname, parent)
    self.source = audio_path
