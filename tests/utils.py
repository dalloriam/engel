class FakeDispatchView(object):
  """
  DEPCRECATED: This fake view aims to help the testing of event dispatchers.
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


class DispatchInterceptorView(object):
  """
  This fake view aims to help the testing of event dispatchers.
  """

  def __init__(self):
    self.is_loaded = True
    self.received_commands = []
    self.received_events = []

  def dispatch(self, cmd):
    self.received_commands.append(cmd)

  def on(self, evt, callback, selector):
    self.received_events.append((evt, callback, selector))
