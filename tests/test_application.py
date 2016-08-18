import sys
sys.path.append('../popeui')

from popeui.application import Application, View
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

  def build(self):
    pass


class StyleView(View):
  title = "style"
  stylesheet = "app.css"

  def build(self):
    self._head.load_stylesheet("yao", StyleView.stylesheet)


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
  a = AppBaseTitle()
  v = BaseView(a)

  assert hasattr(v, "_doc_root")
  assert isinstance(v._doc_root, Document)


def test_view_has_head():
  a = AppBaseTitle()
  v = BaseView(a)

  assert hasattr(v, "_head")


def test_view_has_body():
  a = AppBaseTitle()
  v = BaseView(a)

  assert hasattr(v, "root")
  assert isinstance(v.root, Body)


def test_view_rendering_raises_no_exceptions():
  try:
    a = AppBaseTitle()
    v = BaseView(a)
    v._render()
  except Exception:
    assert False


def test_view_rendering_renders_title():
  a = AppBaseTitle()
  v = BaseView(a)
  o_v = v._render()
  assert '<title id="_page-title">base</title>' in o_v['html']


def test_view_rendering_loads_css():
  a = AppBaseTitle()
  ov = BaseView(a)
  v = StyleView(a)

  o_out = ov._render()
  v_out = v._render()

  assert 'rel="stylesheet"' in v_out['html']
  assert 'rel="stylesheet"' not in o_out['html']


# TODO: test event handling (client events + server events)
