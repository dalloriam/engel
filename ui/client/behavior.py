from compiler import compiler


class Javascript(object):

  def __init__(self, elem_id, event, action, server_action_name=None):
    self.client_event = event
    self.client_action = action
    self.elem_id = elem_id

    self.server_action_name = server_action_name

    self.base = 'document.getElementById("{id}").addEventListener("{event}", function() {{'

  def _generate_event_handler(self):
    return self.base.format(id=self.elem_id, event=self.client_event)

  def compile(self):
    print self.client_action()
    return self._generate_event_handler() + "{code} }});".format(code=compiler.to_javascript(self.client_action()))
