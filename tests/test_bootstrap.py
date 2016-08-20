import sys
sys.path.append('../popeui')

from popeui.widgets.text import Title, Paragraph
from popeui.widgets.media import Image

from popeui.libraries import bootstrap4


def test_bootstrap_has_stylesheet():
  assert hasattr(bootstrap4, 'stylesheets')
  assert len(bootstrap4.stylesheets) > 0


def test_bootstrap_has_scripts():
  assert hasattr(bootstrap4, 'scripts')
  assert len(bootstrap4.scripts) > 0


def test_bootstrap_imagecard():
  imgcard = bootstrap4.ImageCard(id="testID", title="title", text="text", img_url="img_url")
  assert imgcard.attributes['id'] == 'card-testID'

  assert isinstance(imgcard.title, Title)
  assert isinstance(imgcard.image, Image)
  assert isinstance(imgcard.text, Paragraph)


def test_bootstrap_card_columns():
  cc = bootstrap4.CardColumns(id="my")
  assert cc.attributes['class'] == 'card-columns'


def test_bootstrap_container():
  container = bootstrap4.Container(id="container")
  assert container.attributes['class'] == 'container-fluid'
