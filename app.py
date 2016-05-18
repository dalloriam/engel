from ui.application.base import Application, View
from ui.widgets.text import Title, ViewTextLink
from ui.widgets.media import Image
from ui.widgets.structure import List
from ui.widgets.forms import Button

import re
import urllib2


class HomePage(View):

  def __init__(self):
    super(HomePage, self).__init__("index", "Home")
    self.root.add_child(Title("WASSUP"))
    self.root.add_child(ViewTextLink("image-page", "MAH IMAGE PAGE"))
    self.root.add_child(ViewTextLink("form", "MAH FORM PAGE"))


class ImagePage(View):

  def __init__(self):
    super(ImagePage, self).__init__("image-page", "Images")
    self.root.add_child(Title("THERE BE IMAGES"))

    # Get images
    ptrn = r"\bhttps?:\/\/\S+(?:png|jpg)\b"
    req = urllib2.Request("http://www.mountainphotography.com/gallery/", headers={'User-Agent': "Magic Browser"})
    raw = urllib2.urlopen(req).read()

    mylist = List()
    self.root.add_child(mylist)

    for match in set(re.findall(ptrn, raw)[:10]):
      mylist.append(Image(match))


class FormPage(View):

  def __init__(self):
    super(FormPage, self).__init__("form", "Test Form")
    self.root.add_child(Title("MY FORM"))

    self.submit_btn = Button("Test")
    self.root.add_child(self.submit_btn)


class MyApp(Application):

  def __init__(self):
    super(MyApp, self).__init__("MyApp", "MyApp", "favicon.png", HomePage())

    self.pages.append(ImagePage())

    frm = FormPage()
    self.pages.append(frm)

    # TODO: Move server actions to view actions (dunno how)
    frm.submit_btn.on_server_click(self.print_ok)
    self.server_actions["print_ok"] = self.print_ok

  def print_ok(self):
    with open("yao.txt", "a") as outfile:
      outfile.write("ok\n")


app = MyApp()
app.run()
