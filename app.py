from ui.application.base import Application, View, client

from ui.widgets.text import Title
from ui.widgets.media import ViewImageLink, Image, Audio
from ui.widgets.forms import Button
from ui.widgets.structure import Panel

from ui.widgets.abstract import HeadLink

import os


class MonAppConsole(object):

  def __init__(self):
    # do some shit
    pass

  def get_pictures(self):
    return ["app-data/img/" + y for y in filter(lambda filename: any([x in filename for x in ["png", "jpg", "jpeg", "gif"]]), os.listdir("app-data/img"))]

  def get_random_image(self):
    pass


class GalleryView(View):

  def __init__(self, params=None):
    super(GalleryView, self).__init__(name="index", title="Home")

    self.pic_handler = MonAppConsole()

    main_panel = Panel(id="main-panel", classname="content")
    main_panel.add_child(Title(id="page-title", text="Photo Gallery"))
    self.root.add_child(main_panel)

    i = 1
    for img_path in self.pic_handler.get_pictures():
      img_id = "img-" + str(i)
      img_div = Panel(id=img_id + "container", classname="img-container")
      img_div.add_child(ViewImageLink(id=img_id, img_url=img_path, view_name="detail", params={"path": img_path}, classname="clickable"))
      main_panel.add_child(img_div)
      i += 1


class DetailView(View):

  def __init__(self, params=None):
    super(DetailView, self).__init__(name="detail", title="Image Details")
    if params and "path" in params:
      path = params["path"]
      main_panel = Panel(id="main-panel", classname="content")
      self.root.add_child(main_panel)
      main_panel.add_child(Title(id="page-title", text=path))
      img_container = Panel(id="big-img-panel", classname="big-image")
      main_panel.add_child(img_container)
      img_container.add_child(Image(id="big-image", img_url=path, classname="big-image"))

      btn = Button(id="btnSound", text="Play Sound")
      audio = Audio(id="soundEffect", audio_path="app-data/audio.mp3")
      audio.attributes["style"] = "display: none;"
      self.root.add_child(audio)
      self.root.add_child(btn)

      self.on(event="click", control=btn, action=self.client_PlaySound)

  @client
  def client_PlaySound(self, document, console):
    audioElem = document.getElementsByTagName("audio")[0]
    audioElem.play()


class PhotoGalleryApp(Application):

  def __init__(self, debug=False):
    super(PhotoGalleryApp, self).__init__(app_name="PhotoGallery", base_title="PhotoGallery", favicon="app-data/favicon.ico", debug=debug)
    self._head.add_child(HeadLink("style", "stylesheet", "app-data/stylesheet.css"))
    self._head.add_child(HeadLink("style", "stylesheet", "https://fonts.googleapis.com/css?family=Tangerine"))

    self.pages["index"] = GalleryView
    self.pages["detail"] = DetailView


app = PhotoGalleryApp(debug=True)
app.run()
