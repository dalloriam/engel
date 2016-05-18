import json
import logging
from datetime import timedelta


import tornado.ioloop
import tornado.web

from ..widgets.structure import Document, Head, Body
from ..widgets.abstract import PageTitle, HeadLink, Script


def get_post_handler(events, render):
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

    self.document = Document()

    self._head = Head()
    self.page_title = PageTitle(self.base_title)

    self._head.add_child(self.page_title)
    self._head.add_child(HeadLink("shortcut icon", self.favicon))
    self._head.add_child(Script("""function pushAction(s_action) {
  var http = new XMLHttpRequest();
  http.open('POST', 'http://localhost:8080');
  http.addEventListener('readystatechange', function() {
    if (http.readyState == 4 && http.status == 200) {
      console.log('k.');
    }
  });
  http.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
  http.send(JSON.stringify({action: s_action}));
}"""))

    self.document.add_child(self._head)
    self.pages = {}

  def compile(self, page_name, params=None):
    logging.info("Compiling " + str(page_name))
    if page_name in self.pages:
      page = self.pages[page_name](params)
      self.document.add_child(page.root)
      self.page_title.content = self.base_title.format(page.title)
      data = self.document.compile()
      self.document.remove_child(page.root)
      return data

  def run(self):
    logging.info("Starting webserver...")
    listener = get_post_handler(self.server_actions, self.compile)
    tornado.web.Application([(r"/app-data/(.*)", tornado.web.StaticFileHandler, {"path": "app-data"}), (r"/.*", listener)]).listen(8080)
    ioloop = tornado.ioloop.IOLoop.instance()
    set_ping(ioloop, timedelta(seconds=2))
    ioloop.start()


class View(object):

  def __init__(self, name, title):
    self.name = name
    self.title = title

    self.root = Body()
