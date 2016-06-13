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


def get_post_handler(get_events, render):
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

  name = None
  base_title = None
  favicon = None

  def __init__(self, debug=False):

    loglevel = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(format='%(asctime)s - [%(levelname)s] %(message)s', datefmt='%I:%M:%S %p', level=loglevel)


    self.server_events = {}
    self.socket = None

    self.document = Document(id="doc")

    self._head = Head(id="head")
    self.page_title = PageTitle(id="page-title", text="")

    self._head.add_child(self.page_title)
    # TODO: Fix the favicon handling. Maybe render in compile() or run()?
    # self._head.add_child(HeadLink("favicon", "shortcut icon", "app-data/favicon.ico"))

    self.document.add_child(self._head)

    self.current_view = None

    self.views = {}
    self.services = {}

  def get_server_events(self):
    return self.server_events

  def get_client_actions(self, view):
    return [getattr(view, x) for x in dir(view) if hasattr(getattr(view, x), "clientside")]

  def compile(self, page_name, params=None):
    logging.info("Compiling " + str(page_name))
    if page_name in self.views:
      self.current_view = self.views[page_name](ctx=self)
      self.current_view.run(params)
      html = self.current_view.render(root=self.document)
      return html

  def run(self):

    logging.info("Initializing services...")
    for svc in self.services:
      self.services[svc] = self.services[svc]()

    logging.info("Starting webserver...")
    listener = get_post_handler(self.get_server_events, self.compile)
    self.socket = get_socket_listener(self)
    tornado.web.Application([(r"/app-data/(.*)", tornado.web.StaticFileHandler, {"path": "app-data"}), (r"/websocket", self.socket), (r"/.*", listener)]).listen(8080)
    ioloop = tornado.ioloop.IOLoop.current()
    set_ping(ioloop, timedelta(seconds=2))
    # ioloop.start()
    # TODO: Figure out threading model
    t = threading.Thread(target=ioloop.start)
    t.start()


class View(object):

  # TODO: Throw exceptions when name & title not set before run
  name = None
  title = None

  stylesheet = None

  def __init__(self, ctx):

    self.root = Body(id="body")
    self._js_event_root = "window.onload = function() {{ {code} }};"
    self._server_event_root = 'ws = new WebSocket("ws://localhost:8080/websocket");ws.onopen = function() {{ {code} }};'

    self.ctx = ctx

    self.server_events = []
    self.evt_handlers = []

    self.socket_events = {}

  def render(self, root):
    # This allows the view to have access to the application's services

    javascript = {
        "top_level": "",
        "events": "",
        "server_events": ""
    }
    root.add_child(self.root)

    root.update_events()
    self.server_events += root.server_events
    self.evt_handlers += root.event_handlers
    self.socket_events.update(root.socket_events)

    # Compiling methods defined with @client
    for client_action in [getattr(self, x) for x in dir(self) if hasattr(getattr(self, x), "clientside")]:
      action_source = client_action()
      javascript["top_level"] += to_javascript(action_source)

    final_js = "".join(javascript["top_level"]) + self._js_event_root.format(code=javascript["events"] + self._server_event_root.format(code="".join(self.server_events)))
    script = Script(id="main-script", js=final_js)

    root.add_child(script)

    out = root.compile()

    # "Unmount" self from document root
    root.remove_child(self.root)
    root.remove_child(script)

    return out

  def on(self, event, action=None, control=None):
    if not control:
      control = self.root

    control_id = control.attributes["id"]

    # TODO: Validate combinations of action & server_action (action must be client, server must be server, etc.)
    # TODO: Remove possibility for duplicate server_events
    if hasattr(action, "clientside"):
      # Is client event handler, generate client Javascript
      self.evt_handlers.append({"action": action.__name__, "event": event, "id": control_id})
    else:
      # Is server event handler, generate WebSocket code to forward event
      logging.info("Registering WebSocket event...")
      self.server_events.append(generate_websocket_handler(event, control_id))

      if event in self.socket_events:
        self.socket_events[event][control_id] = action
      else:
        self.socket_events[event] = {control_id: action}

