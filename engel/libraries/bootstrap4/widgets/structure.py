from ....widgets.structure import Panel
from ....widgets.media import Image
from ....widgets.text import Title, Paragraph


class Container(Panel):
  """
  Bootstrap Container (container-fluid). Views using the ``bootstrap4`` module should use
  containers instead of :class:`~.widgets.structure.Panel`.
  """
  def build(self):
    super(Container, self).build()
    self.add_class('container-fluid')


class BaseCard(Panel):
  """
  Empty Bootstrap Card.
  """
  def build(self):
    super(BaseCard, self).build()
    self.add_class('card')


class ImageCard(BaseCard):
  """
  Image card, with a title and short description.
  """

  def build(self, title, text, img_url):
    """
    :param title: Title of the card
    :param text: Description of the card
    :param img_url: Image of the card
    """
    super(ImageCard, self).build()
    self.title = Title(id=self.id + "-title", text=title, classname="card-title", size=3, parent=self)

    self.block = Panel(id=self.id + "-block", classname="card-block", parent=self)

    self.image = Image(id=self.id + "-image", img_url=img_url, classname="card-image-top img-fluid", parent=self.block)
    self.text = Paragraph(id=self.id + "-text", text=text, classname="card-text", parent=self.block)


class CardColumns(Panel):
  """
  Display card by columns. Views using the ``bootstrap4`` module should use CardColumns instead of :class:`~.widgets.structure.List` for item display.
  """
  def build(self):
    super(CardColumns, self).build()
    self.add_class('card-columns')
