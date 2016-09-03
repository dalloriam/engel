import sys
import pytest
from tests.utils import DispatchInterceptorView

sys.path.append('../engel')

from engel.widgets.structure import Document, Head, Body, Panel, List
from engel.widgets.abstract import HeadLink


class TestDocumentStructure():

  @pytest.fixture(scope='class')
  def doc(self):
    return Document(id='id', view=3)

  def test_widget_structure_document_html_tag(self, doc):
    assert doc.html_tag == "html", 'Document should set Document.html_tag = "html".'

  def test_widget_structure_document_sets_view(self, doc):
    assert doc.view == 3, 'Document.__init__() should set Document.view.'


class TestHeadStructure():

  @pytest.fixture(scope="class")
  def head(self):
    h = Head(id='id')
    h.view = DispatchInterceptorView()
    return h

  def test_widget_structure_head_html_tag(self, head):
    assert head.html_tag == 'head', 'Head should set Head.html_tag = "head".'

  def test_widget_structure_head_load_script_dispatch(self, head):
    head.load_script('//path')
    assert len(head.view.received_commands) == 1 and head.view.received_commands[0] == {'name': 'script', 'path': '//path'}, 'Head.load_sript() should dispatch a script event.'

  def test_widget_structure_head_load_stylesheet_adds_child(self, head):
    head.load_stylesheet('styleid', '//stylepath')
    assert len(head.children) == 1, 'Head.load_stylesheet should add a child to Head.children.'

  def test_widget_structure_head_load_stylesheet_is_valid(self, head):
    assert isinstance(head.children[0], HeadLink) and head.children[0].target == "//stylepath", 'Head.load_stylesheet should add a HeadLink child to Head.children.'


class TestBodyStructure():

  @pytest.fixture(scope="class")
  def bod(self):
    return Body(id='id')

  def test_widget_structure_body_html_tag(self, bod):
    assert bod.html_tag == "body"


class TestPanelStructure():

  @pytest.fixture(scope="class")
  def pnl(self):
    return Panel(id='id')

  def test_widget_structure_panel_html_tag(self, pnl):
    assert pnl.html_tag == "div"


class TestListStructure():

  @pytest.fixture(scope="class")
  def lst(self):
    return List(id='id')

  def test_widget_structure_list_html_tag(self, lst):
    assert lst.html_tag == "ul"

# No list behavior tests for now b/c list overhaul is coming. TODO:
