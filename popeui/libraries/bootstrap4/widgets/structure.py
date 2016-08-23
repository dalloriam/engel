from ....widgets.structure import Panel
from ....widgets.media import Image
from ....widgets.text import Title, Paragraph


class Container(Panel):
  """
  Bootstrap Container (container-fluid). Views using the ``bootstrap4`` module should use
  containers instead of :class:`~.widgets.structure.Panel`.
  """
  def __init__(self, id, classname=None, parent=None):
    super(Container, self).__init__(id=id, classname=classname, parent=parent)
    self.add_class('container-fluid')


class BaseCard(Container):
  """
  Empty Bootstrap Card.
  """

  def __init__(self, id, classname=None, parent=None):
    super(BaseCard, self).__init__(id="card-" + id, classname=classname, parent=parent)
    self.add_class('card')


class ImageCard(BaseCard):
  """
  Image card, with a title and short description.
  """

  def __init__(self, id, title, text, img_url, classname=None, parent=None):
    """
    :param title: Title of the card
    :param text: Description of the card
    :param img_url: Image of the card
    """
    super(ImageCard, self).__init__(id=id, classname=classname, parent=parent)
    self.title = Title(id=id + "-title", text=title, classname="card-title", size=3, parent=self)

    self.block = Panel(id=id + "-block", classname="card-block", parent=self)

    self.image = Image(id=id + "-image", img_url=img_url, classname="card-image-top img-fluid", parent=self.block)
    self.text = Paragraph(id=id + "-text", text=text, classname="card-text", parent=self.block)


class CardColumns(Panel):
  """
  Display card by columns. Views using the ``bootstrap4`` module should use CardColumns instead of :class:`~.widgets.structure.List` for item display.
  """
  def __init__(self, id, classname=None, parent=None):
    super(CardColumns, self).__init__(id=id, classname=classname, parent=parent)
    self.add_class('card-columns')
