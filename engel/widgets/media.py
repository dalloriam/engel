from .base import BaseElement, BaseContainer

from ..utils import html_property


class Image(BaseElement):
  """
  A simple image widget.
  """

  html_tag = "img"

  source = html_property('src')
  """
  Path of the image file
  """

  def build(self, img_url):
    super(Image, self).build()
    self.source = img_url


class Video(BaseElement):
  """
  A simple video widget, set via ``Video.loop`` to loop by default.
  """

  html_tag = "video"

  source = html_property('src')
  """
  Path of the video file
  """
  loop = html_property('loop')
  """
  Loop the video? ("true" / "false") (defaults to ``"true"``)
  """

  def build(self, vid_url):
    super(Video, self).build()
    self.source = vid_url
    self.loop = 'true'


class ImageLink(BaseContainer):
  """
  An image widget, with the added feature of linking to an external URL.
  """

  html_tag = "a"

  target = html_property('href')
  """
  Target of the link
  """

  def build(self, link, img_url):
    super(ImageLink, self).build()
    self.target = link
    self.add_child(Image(self.id + '-img', img_url=img_url))


class Audio(BaseElement):
  """
  A simple audio widget.
  """

  html_tag = "audio"

  source = html_property('src')
  """
  Path of the audio file
  """

  def build(self, audio_path):
    super(Audio, self).build()
    self.source = audio_path
