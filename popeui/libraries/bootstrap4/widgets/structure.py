from ....widgets.structure import Panel
from ....widgets.media import Image
from ....widgets.text import Title, Paragraph


class Container(Panel):

  def __init__(self, id, classname=None, parent=None):
    classname = "container-fluid " + classname if classname else "container-fluid"
    super(Container, self).__init__(id=id, classname=classname, parent=parent)


class _BaseCard(Container):

  def __init__(self, id, classname=None, parent=None):
    classname = "card " + classname if classname else "card"
    super(_BaseCard, self).__init__(id="card-" + id, classname=classname, parent=parent)


class ImageCard(_BaseCard):

  def __init__(self, id, title, text, img_url, classname=None, parent=None):
    super(ImageCard, self).__init__(id="card-" + id, classname=classname, parent=parent)
    self.title = Title(id="card-" + id + "-title", text=title, classname="card-title", size=3, parent=self)

    self.block = Panel(id="card-" + id + "-block", classname="card-block", parent=self)

    self.image = Image(id="card-" + id + "-image", img_url=img_url, classname="card-image-top img-fluid", parent=self.block)
    self.text = Paragraph(id="card-" + id + "-text", text=text, classname="card-text", parent=self.block)


class CardColumns(Panel):

  def __init__(self, id, classname=None, parent=None):
    classname = "card-columns" + classname if classname else "card-columns"
    super(CardColumns, self).__init__(id=id, classname=classname, parent=parent)
