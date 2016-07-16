import sys
sys.path.append('../popeui')

from popeui.application.base import Application, View
from popeui.widgets.structure import Document, Body


class AppNoBaseTitle(Application):

  def heh(self):
    pass


class AppBaseTitle(Application):
  base_title = "{0}"


class NoNameView(View):

  def heh(self):
    pass


class BaseView(View):
  title = "base"


class StyleView(View):
  title = "style"
  stylesheet = "app.css"


# VIEW TESTS

def test_app_fails_on_title_undefined():
  try:
    AppNoBaseTitle()
    assert False
  except Exception as e:
    assert isinstance(e, NotImplementedError)

  try:
    AppBaseTitle()
  except:
    assert False


def test_view_fails_on_title_undefined():
  try:
    NoNameView("heh")
    assert False
  except Exception as e:
    assert isinstance(e, NotImplementedError)


def test_view_has_document():
  v = BaseView("heh")

  assert hasattr(v, "document")
  assert isinstance(v.document, Document)


def test_view_has_head():
  v = BaseView("heh")

  assert hasattr(v, "_head")


def test_view_has_body():
  v = BaseView("heh")

  assert hasattr(v, "root")
  assert isinstance(v.root, Body)

# TODO: Test javascript generation when the pure-python ast generation is implemented


def test_view_rendering_raises_no_exceptions():
  try:
    a = AppBaseTitle()
    v = BaseView(a)
    v.render()
  except Exception:
    assert False


def test_view_rendering_renders_title():
  a = AppBaseTitle()
  v = BaseView(a)
  o_v = v.render()
  assert '<title id="_page-title">base</title>' in o_v


def test_view_rendering_loads_css():
  a = AppBaseTitle()
  ov = BaseView(a)
  v = StyleView(a)

  o_out = ov.render()
  v_out = v.render()

  assert 'rel="stylesheet"' in v_out
  assert 'rel="stylesheet"' not in o_out


# TODO: test event handling (client events + server events)
