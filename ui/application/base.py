import json
import logging
import inspect
from datetime import timedelta


import tornado.ioloop
import tornado.web

from ..widgets.structure import Document, Head, Body
from ..widgets.abstract import PageTitle, HeadLink, Script

from ..client.behavior import Javascript


def client(func):
  def wrapper(self, *args):
    lines = inspect.getsource(func).splitlines()[2:]
    i = 0
    for char in lines[0]:
      if char == " ":
        i += 1
      else:
        break

    text = "\n".join(map(lambda x: ''.join(list(x)[i:]), lines))
    return text
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


class Application(object):

  def __init__(self, app_name, base_title, favicon, debug=False):
    self.name = app_name

    loglevel = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(format='%(asctime)s - [%(levelname)s] %(message)s', datefmt='%I:%M:%S %p', level=loglevel)

    self.base_title = "{0} | " + base_title
    self.favicon = favicon

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

  def compile(self, page_name, params=None):
    logging.info("Compiling " + str(page_name))
    if page_name in self.pages:
      page = self.pages[page_name](params)
      self.server_actions = page.server_actions
      page.compile_javascript()
      self.document.add_child(page.root)
      self.page_title.content = self.base_title.format(page.title)
      data = self.document.compile()
      self.document.remove_child(page.root)
      return data

  def run(self):
    logging.info("Starting webserver...")
    listener = get_post_handler(self.get_server_actions, self.compile)
    tornado.web.Application([(r"/app-data/(.*)", tornado.web.StaticFileHandler, {"path": "app-data"}), (r"/.*", listener)]).listen(8080)
    ioloop = tornado.ioloop.IOLoop.instance()
    set_ping(ioloop, timedelta(seconds=2))
    ioloop.start()


class View(object):

  def __init__(self, name, title):
    self.name = name
    self.title = title

    self.root = Body(id="body")

    self.server_actions = {}

    # Todo: revamp this shit when compiler supports function definitions.
    # call the compiler on the whole view, modify the transformer (or create a new component)
    # so it removes all non-client function definitions from the AST. Then, have the code generator go through
    # the AST and generate one js function for each python client function, and have it generate
    # the global (document.onload) event listener as well as the sub-document listeners.
    # When this is done, the javascript generator will officially be written in pure python.
    self._js_root = "window.onload = function() {{ {code} }};"
    self.script_elem = None
    self.client_actions = []

  def compile_javascript(self):
    src = self._js_root.format(code="".join([x.compile() for x in self.client_actions]))

    if self.script_elem in self.root.children:
      self.root.children.remove_child(self.script_elem)

    self.script_elem = Script(id="event-script", js=src)
    self.root.add_child(self.script_elem)

  def on(self, event, action=None, control=None, server_action_name=None):
    if not control:
      control = self.root
    js = Javascript(control.attributes["id"], event, action, server_action_name=server_action_name)
    self.client_actions.append(js)
