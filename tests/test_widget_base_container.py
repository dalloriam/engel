import sys
import pytest
from tests.utils import FakeDispatchView

sys.path.append('../engel')

from engel.widgets.base import BaseContainer, BaseElement


class TestBaseContainerStructure():

    @pytest.fixture(scope='module')
    def container(self):
        return BaseContainer(id='id')

    def test_widget_base_container_has_children_array(self, container):
        assert hasattr(container, 'children')


def test_widget_base_container_property_parent_setter():
    fake_parent = BaseContainer(id='id')

    b_elem = BaseContainer(id='id2')
    b_elem.parent = fake_parent
    assert b_elem._parent is fake_parent, 'BaseContainer.parent should set the value of internal BaseContainer._parent'


def test_widget_base_container_property_parent_setter_propagates_view():
    fake_parent = BaseContainer(id='id')
    fake_parent.view = 3

    b_elem_1 = BaseContainer(id='id2')
    b_elem_2 = BaseContainer(id='id3', parent=b_elem_1)
    b_elem_1.parent = fake_parent
    assert b_elem_1.view == 3, 'BaseContainer.parent should propagate parent view to self.'
    assert b_elem_2.view == 3, 'BaseContainer.parent should propagate parent view to children.'


def test_widget_base_container_add_child_adds_child():
    fake_parent = BaseContainer(id='id')

    b_elem = BaseContainer(id='id2')

    fake_parent.add_child(b_elem)
    assert len(fake_parent.children) == 1 and fake_parent.children[0] is b_elem, 'BaseContainer.add_child should add child to BaseContainer.children.'


def test_widget_base_container_add_child_sets_parent():
    fake_parent = BaseContainer(id='id')

    b_elem = BaseContainer(id='id2')

    fake_parent.add_child(b_elem)
    assert b_elem.parent is fake_parent, "BaseContainer.add_child should set the child's parent."


def test_widget_base_container_add_child_dispatches_append():
    view_test = FakeDispatchView({'name': 'append', 'html': '<x id="id">', 'selector': '#id'})
    fake_parent = BaseContainer(id='id')
    fake_parent.view = view_test

    b_elem = BaseElement(id='id')
    b_elem.html_tag = 'x'
    b_elem.autoclosing = True

    fake_parent.add_child(b_elem)
    view_test.verify()


def test_widget_base_container_remove_child_removes_child():
    fake_parent = BaseContainer(id='id')
    b_elem = BaseContainer(id='id2', parent=fake_parent)
    assert len(fake_parent.children) == 1 and fake_parent.children[0] is b_elem
    fake_parent.remove_child(b_elem)
    assert len(fake_parent.children) == 0, "BaseContainer.remove_child should remove child from BaseContainer.children."


def test_widget_base_container_remove_child_unsets_parent():
    fake_parent = BaseContainer(id='id')
    b_elem = BaseContainer(id='id2', parent=fake_parent)
    assert b_elem.parent is fake_parent
    fake_parent.remove_child(b_elem)
    assert b_elem.parent is None, "BaseContainer.remove_child should reset the child's parent to None."


def test_widget_base_container_remove_child_dispatches_remove():
    view_test = FakeDispatchView({'name': 'remove', 'selector': '#id'})
    fake_parent = BaseContainer(id='id')

    b_elem = BaseElement(id='id')

    fake_parent.add_child(b_elem)
    fake_parent.view = view_test
    fake_parent.remove_child(b_elem)
    view_test.verify()


def test_widget_base_container_replace_child_replaces_child():
    fake_parent = BaseContainer(id='id')

    b_elem_1 = BaseElement(id='id1', parent=fake_parent)
    b_elem_2 = BaseElement(id='id2')

    fake_parent.replace_child(b_elem_1, b_elem_2)

    assert len(fake_parent.children) == 1 and fake_parent.children[0] is b_elem_2, 'BaseContainer.replace_child() should replace the child in BaseContainer.children.'


def test_widget_base_container_replace_child_handles_parents():
    fake_parent = BaseContainer(id='id')

    b_elem_1 = BaseElement(id='id1', parent=fake_parent)
    b_elem_2 = BaseElement(id='id2')

    fake_parent.replace_child(b_elem_1, b_elem_2)

    assert b_elem_1.parent is None, "BaseContainer.replace_child() should unset the old child's parent."
    assert b_elem_2.parent is fake_parent, "BaseContainer.replace_child() should set the new child's parent."


def test_widget_base_container_compile_compiles_children():
    fake_parent = BaseContainer(id='id')
    fake_parent.html_tag = 'a'

    b_elem_1 = BaseElement(id='id1', parent=fake_parent)
    b_elem_2 = BaseElement(id='id2', parent=fake_parent)

    b_elem_1.html_tag = 'b'
    b_elem_2.html_tag = 'c'

    assert fake_parent.compile() == '<a id="id"><b id="id1"></b><c id="id2"></c></a>'


def test_widget_base_container_clear_children_removes_all():
    container = BaseContainer(id='id')

    child_1 = BaseElement(id='id', parent=container)
    child_2 = BaseElement(id='id2', parent=container)

    assert len(container.children) == 2
    container.clear_children()
    assert len(container.children) == 0
