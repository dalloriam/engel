import sys
import pytest
from tests.utils import FakeDispatchView

sys.path.append('../engel')

from engel.widgets.base import BaseElement


class BuildTriggerWidget(BaseElement):

    def build(self):
        self._attributes['ok'] = True


class BuildArgsWidget(BaseElement):

    def build(self, hello):
        self._attributes['hello'] = hello


class BuildArgsWidgetOptional(BaseElement):

    def build(self, hello=None):
        self._attributes['hello'] = None


class ViewWidget(BaseElement):

    def on_view_attached(self):
        self._attributes['VIEWATTACH'] = True


class TestBaseElementStructure():

    @pytest.fixture(scope="class")
    def element(self):
        return BaseElement(id='id')

    def test_widget_base_element_has_attributes(self, element):
        assert hasattr(element, '_attributes'), 'BaseElement constructor must define an internal _attributes dictionary.'

    def test_widget_base_element_attributes_is_dict(self, element):
        assert isinstance(element._attributes, dict), 'BaseElement._attributes must be a dictionary.'

    def test_widget_base_element_has_view(self, element):
        assert hasattr(element, '_view'), 'BaseElement constructor must define _view.'

    def test_widget_base_element_view_defaults_to_none(self, element):
        assert element._view is None, 'BaseElement._view should default to None when no parent specified.'

    def test_widget_base_element_has_parent(self, element):
        assert hasattr(element, '_parent'), 'BaseElement constructor must define _parent.'

    def test_widget_base_element_parent_defaults_to_none(self, element):
        assert element._parent is None, 'BaseElement._parent should default to None when no parent specified.'

    def test_widget_base_element_has_class_list(self, element):
        assert hasattr(element, '_classes'), 'BaseElement constructor must define an internal "_classes" list.'

    def test_widget_base_element_classes_default_to_empty(self, element):
        assert element._classes == [], 'BaseElement._list should default to an empty list.'

    def test_widget_base_element_has_autoclosing(self, element):
        assert hasattr(element, 'autoclosing'), 'BaseElement constructor must define the autoclosing attribute.'

    def test_widget_base_element_autoclosing_defaults_to_false(self, element):
        assert element.autoclosing is False, 'BaseElement.autoclosing should default to False'

    def test_widget_base_element_has_content(self, element):
        assert hasattr(element, 'content'), 'BaseElement constructor must define the "content" attribute.'

    def test_widget_base_element_content_is_empty_string(self, element):
        assert element.content == "", 'BaseElement.content should default to an empty string.'


def test_widget_base_element_build_method_gets_called():
    t_elem = BuildTriggerWidget(id='id')
    assert t_elem._attributes.get('ok') is True, 'BaseElement constructor should call the build() method.'


def test_widget_base_element_build_accepts_parameters():
    t_elem = BuildArgsWidget(id='id', hello='12345')
    assert t_elem._attributes.get('hello') == '12345', 'BaseElement constructor should forward **kwargs to the build() method.'


def test_widget_base_element_property_view_getter():
    b_elem = BaseElement(id='id')
    assert b_elem.view is b_elem._view, 'BaseElement.view should return the value of internal BaseElement._view.'


def test_widget_base_element_property_view_setter():
    b_elem = BaseElement(id='id')
    b_elem.view = 42
    assert b_elem._view == 42, 'BaseElement.view should set the value of internal BaseElement._view'


def test_widget_base_element_property_view_setter_calls_on_view_attached():
    t_elem = ViewWidget(id='id')
    t_elem.view = 3
    assert t_elem._attributes.get('VIEWATTACH') is True, 'BaseElement.view should call on_view_attached() when view is not None'


def test_widget_base_element_property_view_setter_doesnt_call_onview_when_view_is_none():
    t_elem = ViewWidget(id='id')
    t_elem.view = None
    assert 'VIEWATTACH' not in t_elem._attributes, 'BaseElement.view should not call on_view_attached() when view is None'


def test_widget_base_element_property_parent_getter():
    b_elem = BaseElement(id='id')
    assert b_elem.parent is b_elem._parent, 'BaseElement.parent should return the value of internal BaseElement._parent'


def test_widget_base_element_property_parent_setter():
    fake_parent = BaseElement(id='id')

    b_elem = BaseElement(id='id2')
    b_elem.parent = fake_parent
    assert b_elem._parent is fake_parent, 'BaseElement.parent should set the value of internal BaseElement._parent'


def test_widget_base_element_property_parent_setter_sets_view():
    fake_parent = BaseElement(id='id')
    fake_parent.view = 3

    b_elem = BaseElement(id='id2')
    b_elem.parent = fake_parent
    assert b_elem.view == 3, "BaseElement.parent should set the value of BaseElement.view to the parent's view"


def test_widget_base_element_sets_attributes():
    b_elem = BaseElement(id='id')
    b_elem._set_attribute('hello', 'there')
    assert b_elem._attributes.get('hello') == 'there', "BaseElement._set_attribute should set the specified attribute in BaseElement._attributes"


def test_widget_base_element_doesnt_set_attribute_when_none():
    b_elem = BaseElement(id='id')
    b_elem._set_attribute('hello', None)
    assert 'hello' not in b_elem._attributes, 'BaseElement._set_attribute should do nothing when attribute value is None'


def test_widget_base_element_attribute_dispatches_when_view_exists():
    view = FakeDispatchView({'name': 'attr', 'selector': '#id', 'attr': 'hello', 'value': 'world'})

    b_elem = BaseElement(id='id')
    b_elem.view = view
    b_elem._set_attribute('hello', 'world')
    view.verify()


def test_widget_base_element_property_id():
    b_elem = BaseElement(id='id')
    assert b_elem.id == 'id', 'BaseElement.id should return the value of internal BaseElement._attributes["id"]'


def test_widget_base_element_property_id_setter():
    b_elem = BaseElement(id='id')
    b_elem.id = 'id2'
    assert b_elem.id == 'id2', 'BaseElement.id should set the value of BaseElement._attributes["id"]'


def test_widget_base_element_classname_is_set():
    b_elem = BaseElement(id='hello', classname="hello")
    err = 'BaseElement constructor should be able to set a class via the "classname" keyword arg.'

    assert len(b_elem._classes) == 1, err
    assert b_elem._classes[0] == "hello", err


def test_widget_base_element_property_classname_getter():
    b_elem = BaseElement(id='hello', classname="hello")
    assert b_elem.classname == "hello", 'BaseElement.classname should return an aggregate of BaseElement._classes.'


def test_widget_base_element_remove_class_removes_class():
    b_elem = BaseElement(id='id', classname='hello')
    b_elem.remove_class('hello')
    assert len(b_elem._classes) == 0, 'BaseElement.remove_class() should delete specified class from BaseElement._classes.'


def test_widget_base_element_compile_autoclosing():
    b_elem = BaseElement(id='a')
    b_elem.html_tag = "x"
    b_elem.autoclosing = True
    assert b_elem.compile() == '<x id="a">'


def test_widget_base_element_compile_not_autoclosing():
    b_elem = BaseElement(id='a')
    b_elem.html_tag = 'x'
    b_elem.content = "b"
    assert b_elem.compile() == '<x id="a">b</x>'
