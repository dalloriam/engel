import os
import shutil
import json

import tornado.ioloop
import tornado.web

from ..widgets.structure import Document, Head, Body
from ..widgets.abstract import PageTitle, HeadLink, Script


def get_post_handler(events):
  class ServerActionHandler(tornado.web.RequestHandler):

    def post(self):
      raw = json.loads(self.request.body)
      action = raw["action"]
      if action in events:
        events[action]()
  return ServerActionHandler


class Application(object):

  def __init__(self, app_name, base_title, favicon, root_page):
    self.name = app_name

    self.root_path = os.path.abspath(self.name + "/" + root_page.name + ".html")

    self.base_title = "{0} | " + base_title
    self.favicon = favicon

    self.server_actions = {}

    self.document = Document()

    self._head = Head()
    self.page_title = PageTitle(self.base_title)

    self._head.add_child(self.page_title)
    self._head.add_child(HeadLink("icon", self.favicon))
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
    self.pages = [root_page]

  def compile(self):
    print("Checking for app directory...")
    if os.path.isdir(self.name):
      print("App directory exists. Deleting...")
      shutil.rmtree(self.name)

    print("Creating app directory...")
    os.mkdir(self.name)

    print("Copying files...")
    shutil.copy(self.favicon, self.name)

    print("Rendering pages...")
    i = 1
    max = len(self.pages)

    for page in self.pages:
      print("{0}/{1}".format(i, max))
      self.document.add_child(page.root)
      self.page_title.content = self.base_title.format(page.title)

      with open(self.name + "/" + page.name + ".html", "a") as outfile:
        outfile.write(self.document.compile())
      self.document.remove_child(page.root)
      i += 1

    print("Rendering done.")

  def run(self):
    self.compile()

    print("Starting web server...")
    listener = get_post_handler(self.server_actions)
    tornado.web.Application([(r"/.*", listener), ]).listen(8080)
    tornado.ioloop.IOLoop.instance().start()

    print("Starting browser...")
    os.system('start chrome "file://{0}" --kiosk'.format(self.root_path))


class View(object):

  def __init__(self, name, title):
    self.name = name
    self.title = title

    self.root = Body()
