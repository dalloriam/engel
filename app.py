from ui.application.base import Application, View, client

from ui.widgets.text import Title
from ui.widgets.media import ViewImageLink, Image
from ui.widgets.forms import Button

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

    self.root.add_child(Title(id="page-title", text="Photo Gallery"))

    i = 1
    for img_path in self.pic_handler.get_pictures():
      img_id = "img-" + str(i)
      self.root.add_child(ViewImageLink(id=img_id, img_url=img_path, view_name="detail", params={"path": img_path}))
      i += 1


class DetailView(View):

  def __init__(self, params=None):
    super(DetailView, self).__init__(name="detail", title="Image Details")
    if params and "path" in params:
      path = params["path"]
      self.root.add_child(Title(id="page-title", text=path))
      self.root.add_child(Image(id="big-image", img_url=path))

      btn = Button(id="btnSmaller", text="Make Smaller")
      self.root.add_child(btn)

      self.on(event="click", control=btn, action=self.client_Manipulate)

  @client
  def client_Manipulate(self, document, console):
    if "x" not in "yao":
      my_img = document.getElementsByTagName("img")[0]
      my_img.style.width = "80%"


class PhotoGalleryApp(Application):

  def __init__(self, debug=False):
    super(PhotoGalleryApp, self).__init__(app_name="PhotoGallery", base_title="PhotoGallery", favicon="/appdata/favicon.ico", debug=debug)

    self.pages["index"] = GalleryView
    self.pages["detail"] = DetailView


app = PhotoGalleryApp(debug=True)
app.run()
