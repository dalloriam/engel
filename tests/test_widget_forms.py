import sys
import pytest
from tests.utils import DispatchInterceptorView

sys.path.append('../engel')

from engel.widgets.forms import Button, TextBox


class TestButtonStructure():

  @pytest.fixture(scope="class")
  def btn(self):
    return Button(id='id', text='clickme')

  def test_widget_forms_button_html_tag(self, btn):
    assert btn.html_tag == 'button', 'Button should set Button.html_tag = "button".'

  def test_widget_forms_button_sets_content(self, btn):
    assert btn.content == 'clickme', 'Button.build() should set Button.content.'


class TestTextboxStructure():

  @pytest.fixture(scope="class")
  def txt(self):
    return TextBox(id='id', name='myname')

  def test_widget_forms_textbox_html_tag(self, txt):
    assert txt.html_tag == 'input', 'TextBox should set TextBox.html_tag = "input".'

  def test_widget_forms_textbox_has_text(self, txt):
    assert hasattr(txt, 'text') and isinstance(txt.__class__.text, property), 'TextBox should have a property TextBox.text.'

  def test_widget_forms_textbox_has_input_type(self, txt):
    assert hasattr(txt, 'input_type') and isinstance(txt.__class__.input_type, property), 'TextBox should have a property TextBox.input_type.'

  def test_widget_forms_textbox_has_name(self, txt):
    assert hasattr(txt, 'name') and isinstance(txt.__class__.name, property), 'TextBox should have a property TextBox.name.'

  def test_widget_forms_textbox_sets_text(self, txt):
    assert txt.text == "", 'TextBox.build() should set TextBox.text = "".'

  def test_widget_forms_textbox_sets_input_type(self, txt):
    assert txt.input_type == "text", 'TextBox.build() should set TextBox.input_type = "text".'

  def test_widget_forms_textbox_sets_name(self, txt):
    assert txt.name == "myname", 'TextBox.build() should set TextBox.name.'


class TestTextboxBehavior():

  @pytest.fixture()
  def txt(self):
    v = DispatchInterceptorView()
    txt = TextBox(id='id', name='myname')
    txt.view = v
    return txt

  def test_widget_forms_textbox_text_dispatches_update(self, txt):
    txt.text = "hello"
    assert len(txt.view.received_commands) == 1 and txt.view.received_commands[0] == {'name': 'text', 'selector': '#' + txt.id, 'text': "hello"}, "Setting TextBox.text should dispatch an event if a view is attached."

  def test_widget_forms_textbox_text_escapes_html(self, txt):
    txt.text = "<h1>hello</h1>"
    assert txt.text == "&lt;h1&gt;hello&lt;/h1&gt;", "Setting TextBox.text should escape HTML."

  def test_widget_forms_textbox_registers_change_event(self, txt):
    assert len(txt.view.received_events) == 1
    evt = txt.view.received_events[0]
    assert evt[0] == 'change' and callable(evt[1]) and evt[2] == '#id', 'TextBox.on_view_attached() should register the "change" event.'
