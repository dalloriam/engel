from ui.application.base import Application, View
from ui.widgets.text import Title, ViewTextLink
from ui.widgets.media import Image
from ui.widgets.structure import List

import re
import urllib2


class HomePage(View):

  def __init__(self):
    super(HomePage, self).__init__("index", "Home")
    self.root.add_child(Title("WASSUP"))
    self.root.add_child(ViewTextLink("image-page", "MAH IMAGE PAGE"))


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


class MyApp(Application):

  def __init__(self):
    super(MyApp, self).__init__("MyApp", "MyApp", "favicon.png", HomePage())
    self.pages.append(ImagePage())


app = MyApp()
app.run()
