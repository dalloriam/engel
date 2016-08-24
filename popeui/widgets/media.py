from .base import BaseElement, BaseContainer

from ..utils import html_property


class Image(BaseElement):
  """
  A simple image widget.
  """

  html_tag = "img"

  source = html_property('src')

  def build(self, img_url):
    self.source = img_url


class Video(BaseElement):
  """
  A simple video widget, set via ``Video.loop`` to loop by default.
  """

  html_tag = "video"

  source = html_property('src')
  loop = html_property('loop')

  def build(self, vid_url):
    self.source = vid_url
    self.loop = 'true'


class ImageLink(BaseContainer):
  """
  An image widget, with the added feature of linking to an external URL.
  """

  html_tag = "a"

  target = html_property('href')

  def build(self, link, img_url):
    self.target = link
    self.add_child(Image(self.id + '-img', img_url=img_url))


class Audio(BaseElement):
  """
  A simple audio widget.
  """

  html_tag = "audio"

  source = html_property('src')

  def build(self, audio_path):
    self.source = audio_path
