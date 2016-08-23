import sys
sys.path.append('../popeui')

from popeui.widgets import Panel, Span


class FakeDispatchView(object):
  """
  This fake view aims to help the testing of event dispatchers.
  """

  def __init__(self, expected_command):
    self.expected_command = expected_command
    self.is_loaded = True

    self.was_dispatched = False

  def dispatch(self, cmd):
    self.was_dispatched = True
    assert self.expected_command == cmd

  def verify(self):
    assert self.was_dispatched


def test_event_append_child():

  expected = {
    'name': 'append',
    'html': '<span id="my-span">oki</span>',
    'selector': '#main-panel'
  }

  verifier = FakeDispatchView(expected)

  parent = Panel(id="main-panel")
  parent.view = verifier

  child = Span(id="my-span", text="oki")
  parent.add_child(child)
  verifier.verify()

def test_event_remove_child():

  expected = {
    'name': 'remove',
    'selector': '#my-span'
  }

  verifier = FakeDispatchView(expected)

  parent = Panel(id='main-panel')

  child = Span(id="my-span", text='oki')
  parent.add_child(child)
  parent.view = verifier

  parent.remove_child(child)
  verifier.verify()


def test_event_replace_child():

  expected = {
    'name': 'replace',
    'html': '<span id="my-other-span">hello</span>',
    'selector': '#my-span'
  }

  verifier = FakeDispatchView(expected)

  parent = Panel(id="main-panel")

  child1 = Span(id="my-span", text="oki")
  parent.add_child(child1)

  parent.view = verifier

  child2 = Span(id="my-other-span", text="hello")

  parent.replace_child(child1, child2)
  verifier.verify()


def test_event_add_class():

  expected = {
    'name': 'addclass',
    'cl': 'hue',
    'selector': '#my-span'
  }

  verifier = FakeDispatchView(expected)

  child = Span(id='my-span', text="oki")
  child.view = verifier

  child.add_class('hue')
  verifier.verify()

def test_event_remove_class():

  expected = {
    'name': 'removeclass',
    'cl': 'hue',
    'selector': '#my-span'
  }

  verifier = FakeDispatchView(expected)

  child = Span(id='my-span', text='oki', classname='hue')
  child.view = verifier

  child.remove_class('hue')
  verifier.verify()


def test_event_set_attr():

  expected = {
    'name': 'attr',
    'selector': '#my-span',
    'attr': 'hello',
    'value': 'world'
  }

  verifier = FakeDispatchView(expected)

  child = Span(id='my-span', text='oki')
  child.view = verifier

  child._set_attribute('hello', 'world')
  verifier.verify()
