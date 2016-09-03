import sys
import pytest

sys.path.append('../engel')

from engel.libraries.bootstrap4.widgets.structure import Container, BaseCard, CardColumns, ImageCard

from engel.widgets import Title, Image, Panel, Paragraph


class TestContainerStructure():

  @pytest.fixture(scope="class")
  def cont(self):
    return Container(id='id')

  def test_bootstrap4_widgets_structure_container_has_class(self, cont):
    assert 'container-fluid' in cont._classes, 'bootstrap4.Container.build() should add the class "container-fluid".'


class TestBaseCardStructure():

  @pytest.fixture(scope="class")
  def card(self):
    return BaseCard(id='id')

  def test_bootstrap4_widgets_structure_basecard_has_class(self, card):
    assert 'card' in card._classes, 'bootstrap4.Container.build() should add the class "card".'


class TestCardColumnsStructure():

  @pytest.fixture(scope="class")
  def cols(self):
    return CardColumns(id='id')

  def test_bootstrap4_widgets_structure_cardcolumns_has_class(self, cols):
    assert 'card-columns' in cols._classes, 'bootstrap4.Container.build() should add the class "card-columns".'


class TestImageCardStructure():

  @pytest.fixture(scope="class")
  def card(self):
    return ImageCard(id='id', title='title', text='mytext', img_url='//url')

  def test_bootstrap4_widgets_structure_imagecard_has_valid_title(self, card):
    assert hasattr(card, 'title') and isinstance(card.title, Title) and card.title.content == 'title', 'bootstrap4.Container.build() should have an attribute Container.title set as a Title.'

  def test_bootstrap4_widgets_structure_imagecard_has_valid_description(self, card):
    assert hasattr(card, 'text') and isinstance(card.text, Paragraph) and card.text.content == 'mytext', 'bootstrap4.Container.build() should have an attribute Container.text set as a Paragraph.'

  def test_bootstrap4_widgets_structure_imagecard_has_valid_image(self, card):
    assert hasattr(card, 'image') and isinstance(card.image, Image) and card.image.source == '//url', 'bootstrap4.Container.build() should have an attribute Container.image set as an Image.'

  def test_bootstrap4_widgets_structure_imagecard_has_valid_block(self, card):
    assert hasattr(card, 'block') and isinstance(card.block, Panel), 'bootstrap4.Container.build() should have an attribute Container.block set as a Panel.'

  def test_bootstrap4_widgets_structure_imagecard_widget_inheritance(self, card):
    assert card.block.parent is card, 'bootstrap4.Container.block should be set as child of bootstrap4.Container.'
    assert card.image.parent is card.block, 'bootstrap4.Container.image should be set as child of bootstrap4.Container.block.'
    assert card.text.parent is card.block, 'bootstrap4.Container.text should be set as child of bootstrap4.Container.block.'
