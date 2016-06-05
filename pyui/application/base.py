import json
import logging
import inspect
from datetime import timedelta


import tornado.ioloop
import tornado.web

import threading

from ..widgets.structure import Document, Head, Body
from ..widgets.abstract import PageTitle, HeadLink, Script

from ..client.compiler.compiler import to_javascript, generate_event_handler


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

    def post(self):
      raw = json.loads(self.request.body)
      action = raw["action"]
      events = get_events()
      if action in events:
        events[action]()
  return ServerActionHandler


def set_ping(ioloop, timeout):
  ioloop.add_timeout(timeout, lambda: set_ping(ioloop, timeout))


class WebSocketListener(tornado.websocket.WebSocketHandler):

  def _configure(self, parse_fn):
    self.parse = parse_fn

  def open(self):
    print("WebSocket Opened.")

  def on_message(self, message):
    pass

  def close(self):
    print("WebSocket Closed.")


class Application(object):

  def __init__(self, app_name, base_title, favicon, debug=False):
    self.name = app_name

    loglevel = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(format='%(asctime)s - [%(levelname)s] %(message)s', datefmt='%I:%M:%S %p', level=loglevel)

    self.base_title = "{0} | " + base_title
    self.favicon = favicon

    # Todo: revamp this shit when compiler supports function definitions.
    # call the compiler on the whole view, modify the transformer (or create a new component)
    # so it removes all non-client function definitions from the AST. Then, have the code generator go through
    # the AST and generate one js function for each python client function, and have it generate
    # the global (document.onload) event listener as well as the sub-document listeners.
    # When this is done, the javascript generator will officially be written in pure python.
    self._js_root = "window.onload = function() {{ {code} }};"
    self.server_actions = {}

    self.document = Document(id="doc")

    self._head = Head(id="head")
    self.page_title = PageTitle(id="page-title", text=self.base_title)

    self._head.add_child(self.page_title)
    self._head.add_child(HeadLink("favicon", "shortcut icon", "app-data/favicon.ico"))

    self.document.add_child(self._head)
    self.pages = {}

  def get_server_actions(self):
    return self.server_actions

  def get_client_actions(self, view):
    return [getattr(view, x) for x in dir(view) if hasattr(getattr(view, x), "clientside")]

  def compile(self, page_name, params=None):
    logging.info("Compiling " + str(page_name))
    if page_name in self.pages:
      page = self.pages[page_name](params)
      self.server_actions = page.server_actions
      self.document.add_child(page.root)
      raw_js = ""
      for action in self.get_client_actions(page):
        src = action()
        raw_js += to_javascript(src)
      raw_js += self._js_root.format(code=page.render_events())

      sc_elem = Script("main-script", raw_js)
      self._head.add_child(sc_elem)

      print(self.get_client_actions(page))
      self.page_title.content = self.base_title.format(page.title)
      data = self.document.compile()
      self.document.remove_child(page.root)
      self._head.remove_child(sc_elem)
      return data

  def update_element(self, element):
    pass

  def run(self):
    logging.info("Starting webserver...")
    listener = get_post_handler(self.get_server_actions, self.compile)

    self.web_socket_listener = WebSocketListener()
    self.web_socket_listener.configure(self.update_element)

    tornado.web.Application([(r"/app-data/(.*)", tornado.web.StaticFileHandler, {"path": "app-data"}), (r"/websocket", self.web_socket_listener), (r"/.*", listener)]).listen(8080)
    ioloop = tornado.ioloop.IOLoop.current()
    set_ping(ioloop, timedelta(seconds=2))
    ioloop.start()
    # TODO: Figure out threading model
    # t = threading.Thread(target=ioloop.start)
    # t.start()


class View(object):

  def __init__(self, name, title):
    self.name = name
    self.title = title

    self.root = Body(id="body")

    self.server_actions = {}

    self.evt_handlers = []

  def render_events(self):
    out = ""
    for evt in self.evt_handlers:
      out += generate_event_handler(evt["event"], evt["id"], evt["action"])
    return out

  def on(self, event, action_name=None, control=None):
    if not control:
      control = self.root

    self.evt_handlers.append({"action": action_name, "event": event, "id": control.attributes["id"]})
