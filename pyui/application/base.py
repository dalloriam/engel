import json
import logging
import inspect
from datetime import timedelta


import tornado.ioloop
import tornado.web
import tornado.websocket

from .websocket import get_socket_listener

import threading

from ..widgets.structure import Document, Head, Body
from ..widgets.abstract import PageTitle, HeadLink, Script

from ..client.compiler.compiler import to_javascript, generate_event_handler, generate_websocket_handler


def client(func):
  def wrapper(*args):
    lines = inspect.getsource(func).splitlines()[1:]
    i = 0
    for char in lines[0]:
      if char == " ":
        i += 1
      else:
        break

    text = "\n".join(map(lambda x: ''.join(list(x)[i:]), lines))
    return text
  wrapper.clientside = True
  wrapper.__name__ = func.__name__
  return wrapper


def get_post_handler(render):
  class ServerActionHandler(tornado.web.RequestHandler):

    def get(self):
      split_url = self.request.uri.split("?")
      if len(split_url) == 1:
        page = split_url[0].replace("/", "")
        data = render(page)
        if data:
          self.write(data)
      else:
        page_string, param_string = split_url
        page = page_string.replace("/", "")
        params = {k[0]: k[1] for k in map(lambda x: x.split("="), param_string.split("&"))}
        data = render(page, params)
        if data:
          self.write(render(page, params))
  return ServerActionHandler


def set_ping(ioloop, timeout):
  ioloop.add_timeout(timeout, lambda: set_ping(ioloop, timeout))


class Application(object):

  base_title = None
  favicon = None

  def __init__(self, debug=False):

    loglevel = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(format='%(asctime)s - [%(levelname)s] %(message)s', datefmt='%I:%M:%S %p', level=loglevel)

    if self.base_title is None:
      raise NotImplementedError

    self.socket = None

    self.current_view = None

    self.views = {}
    self.services = {}

  def compile(self, page_name, params=None):
    logging.info("Compiling " + str(page_name))
    if page_name in self.views:
      self.current_view = self.views[page_name](ctx=self)
      self.current_view.run(params)
      html = self.current_view.render()
      return html

  def run(self):

    logging.info("Initializing services...")
    for svc in self.services:
      self.services[svc] = self.services[svc]()

    logging.info("Starting webserver...")
    listener = get_post_handler(self.compile)
    self.socket = get_socket_listener(self)
    tornado.web.Application([(r"/app-data/(.*)", tornado.web.StaticFileHandler, {"path": "app-data"}), (r"/websocket", self.socket), (r"/.*", listener)]).listen(8080)
    ioloop = tornado.ioloop.IOLoop.current()
    set_ping(ioloop, timedelta(seconds=2))
    # TODO: This can't be properly stopped on windows, check for fix
    t = threading.Thread(target=ioloop.start)
    t.start()


class View(object):

  title = None

  stylesheet = None

  def __init__(self, ctx):

    if self.title is None:
      raise NotImplementedError

    self.document = Document(id="doc")

    self._head = Head(id="head", parent=self.document)

    self.root = Body(id="body", parent=self.document)

    # TODO: Move this to AST generation, this will allow to get rid of all the hardcoded javascript
    self._js_event_root = "window.onload = function() {{ {code} }};"
    self._server_event_root = 'ws = new WebSocket("ws://localhost:8080/websocket");ws.onopen = function() {{ {code} }};'

    self.ctx = ctx

    self.server_events = []
    self.evt_handlers = []

    self.socket_events = {}

  def render(self):

    javascript = {
        "top_level": "",
        "events": "",
        "server_events": ""
    }

    self.document.update_events()
    self.server_events += self.document.server_events
    self.evt_handlers += self.document.event_handlers
    self.socket_events.update(self.document.socket_events)

    if self.stylesheet:
      HeadLink(id="style", link_type="stylesheet", path=self.stylesheet, parent=self._head)

    PageTitle(id="_page-title", text=self.ctx.base_title.format(self.title), parent=self._head)

    # Compiling methods defined with @client
    for client_action in [getattr(self, x) for x in dir(self) if hasattr(getattr(self, x), "clientside")]:
      action_source = client_action()
      javascript["top_level"] += to_javascript(action_source)

    final_js = "".join(javascript["top_level"]) + self._js_event_root.format(code="".join(self.evt_handlers) + self._server_event_root.format(code="".join(self.server_events)))
    script = Script(id="main-script", js=final_js, parent=self._head)

    return self.document.compile()

  def on(self, event, control=None, action=None):
    if not control:
      control = self.root

    control_id = control.attributes["id"]

    # TODO: Remove possibility for duplicate server_events
    if hasattr(action, "clientside"):
      # Is client event handler, generate client Javascript
      self.evt_handlers.append(generate_event_handler(event, control_id, action.__name__))
    else:
      # Is server event handler, generate WebSocket code to forward event
      logging.info("Registering WebSocket event...")
      self.server_events.append(generate_websocket_handler(event, control_id))

      if event in self.socket_events:
        self.socket_events[event][control_id] = action
      else:
        self.socket_events[event] = {control_id: action}

