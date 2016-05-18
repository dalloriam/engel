from ui.application.base import Application, View
from ui.widgets.text import Title
from ui.widgets.media import ViewImageLink, Image

import os


class MonAppConsole(object):

  def __init__(self):
    # do some shit
    pass

  def get_pictures(self):
    return ["app-data/img/" + y for y in filter(lambda filename: any([x in filename for x in ["png", "jpg", "jpeg", "gif"]]), os.listdir("app-data/img"))]


class GalleryView(View):

  def __init__(self, params=None):
    super(GalleryView, self).__init__(name="index", title="Home")

    self.pic_handler = MonAppConsole()

    self.root.add_child(Title(text="Photo Gallery"))

    for img_path in self.pic_handler.get_pictures():
      self.root.add_child(ViewImageLink(img_url=img_path, view_name="detail", params={"path": img_path}))


class DetailView(View):

  def __init__(self, params=None):
    super(DetailView, self).__init__(name="detail", title="Image Details")
    if params and "path" in params:
      path = params["path"]
      self.root.add_child(Title(text=path))
      self.root.add_child(Image(img_url=path))


class PhotoGalleryApp(Application):

  def __init__(self, debug=False):
    super(PhotoGalleryApp, self).__init__(app_name="PhotoGallery", base_title="PhotoGallery", favicon="/appdata/favicon.ico", debug=debug)

    self.pages["index"] = GalleryView
    self.pages["detail"] = DetailView


app = PhotoGalleryApp(debug=True)
app.run()
