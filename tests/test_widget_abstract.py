import sys
import pytest

sys.path.append('../engel')

from engel.widgets.abstract import HeadLink, PageTitle, Script


class TestHeadLinkStructure():

  @pytest.fixture(scope="class")
  def headlink(self):
    return HeadLink(id='id', link_type="stylesheet", path="/test")

  def test_widget_abstract_headlink_html_tag(self, headlink):
    assert headlink.html_tag == "link", 'HeadLink should set HeadLink.html_tag = "link".'

  def test_widget_abstract_headlink_has_target(self, headlink):
    assert hasattr(headlink, 'target') and isinstance(headlink.__class__.target, property), 'HeadLink should have a property HeadLink.target.'

  def test_widget_abstract_headlink_has_link_type(self, headlink):
    assert hasattr(headlink, 'link_type') and isinstance(headlink.__class__.target, property), 'HeadLink should have a property HeadLink.link_type.'

  def test_widget_abstract_headlink_sets_target(self, headlink):
    assert headlink.target == '/test', 'HeadLink.build() should set HeadLink.target.'

  def test_widget_abstract_headlink_sets_link_type(self, headlink):
    assert headlink.link_type == 'stylesheet', 'HeadLink.build() should set HeadLink.link_type'


def TestPageTitleStructure():

  @pytest.fixture(scope="class")
  def title():
    return PageTitle(id='id', text='test')

  def test_widget_abstract_pagetitle_html_tag(self, title):
    assert title.html_tag == 'title', 'PageTitle should set PageTitle.html_tag = "title"'

  def test_widget_abstract_pagetitle_sets_content(self, title):
    assert title.content == 'test', 'PageTitle.build() should set PagetTitle.content.'


def TestScriptStructure():
  @pytest.fixture(scope="class")
  def script():
    return Script(js_path="//js")

  def test_widget_abstract_script_html_tag(self, script):
    assert script.html_tag == 'script', 'Script should set Script.html_tag = "script".'

  def test_widget_abstract_script_has_source(self, script):
    assert hasattr('source', script) and isinstance(script.__class__.source, property)

  def test_widget_abstract_script_sets_source(self, script):
    assert script.source == '//js', "Script.build() should set Script.source."
