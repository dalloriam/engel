import sys
import pytest
sys.path.append('../engel')

from engel.application import View, Application
from engel.widgets.structure import Document, Head


class TestViewStructure():

  @pytest.fixture(scope="class")
  def no_title(self):
    class MyView(View):
      pass
    return MyView

  @pytest.fixture(scope="class")
  def view_base(self, app_base):
    class MyView(View):
      title = "Home"

    return MyView(app_base)

  @pytest.fixture(scope="class")
  def app_base(self):
    class MyApp(Application):
      base_title = "{0} | Base"
    return MyApp()

  def test_view_raises_when_no_title(self, no_title, app_base):
    with pytest.raises(NotImplementedError):
      no_title(app_base)

  def test_view_sets_isloaded(self, view_base):
    assert hasattr(view_base, 'is_loaded') and view_base.is_loaded is False, 'View should set View.is_loaded = False.'

  def test_view_sets_docroot(self, view_base):
    assert hasattr(view_base, '_doc_root') and isinstance(view_base._doc_root, Document), 'View should set View._doc_root.'

  def test_view_sets_head(self, view_base):
    assert hasattr(view_base, '_head') and isinstance(view_base._head, Head), 'View should set View._head.'
