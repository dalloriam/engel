"""
Contains all the classes and functions related to the structure of a PopeUI application.
"""
import logging
import inspect
from datetime import timedelta


import tornado.ioloop
import tornado.web
import tornado.websocket

from .websocket import _get_socket_listener

import threading

from .widgets.structure import Document, Head, Body
from .widgets.abstract import PageTitle, HeadLink, Script

from .client.compiler.compiler import to_javascript, generate_event_handler, generate_websocket_handler


def client(func):
  """
  Decorator used to declare a client-side javascript function.
  Functions wrapped by this decorator will never be executed as python code,
  but will be compiled to javascript and sent along the HTML returned by :meth:`~.View.render`.

  :param func: Function to decorate.
  :returns: Decorated function now returning the python source code of the original function.
  """
  def wrapper(*args):
    """
    Client method. Will be compiled to javascript and run in the browser.
    """
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


def _get_post_handler(render):
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


def _set_ping(ioloop, timeout):
  ioloop.add_timeout(timeout, lambda: _set_ping(ioloop, timeout))


class Application(object):
  """
  The ``Application`` abstract class represents the entirety of a PopeUI application.

  Your application should inherit from this class and redefine the specifics, like Views, Services,
  and any additional logic required by your project.
  """

  base_title = None
  """
  Page title pattern for the whole application. Gets set on a per-view basis by ``Application.base_title.format(view.title)``.
  """

  # TODO: Add favicon

  def __init__(self, debug=False):
    """
    Constructor of the Application.

    :param debug: Sets the logging level of the application
    :raises NotImplementedError: When ``Application.base_title`` not set in the class definition.
    """
    loglevel = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(format='%(asctime)s - [%(levelname)s] %(message)s', datefmt='%I:%M:%S %p', level=loglevel)

    if self.base_title is None:
      raise NotImplementedError

    self.socket = None

    self.current_view = None

    self.views = {}
    self.services = {}

  def compile(self, page_name, params=None):
    """
    Called by the tornado server. Compiles the view requested by the user by calling its :meth:`~.View.render` method.

    :param page_name: Name of the page to compile
    :param params: parameters to pass to the page
    :returns: Either a HTML string or ``None`` (when the page does not exist)
    """
    logging.info("Compiling " + str(page_name))
    if page_name in self.views:
      self.current_view = self.views[page_name](context=self)
      self.current_view.run(params)
      html = self.current_view.render()
      return html

  def run(self):
    """
    Start the PopeUI application by initializing all registered services and starting a tornado IOLoop in a seperate thread.
    """
    logging.info("Initializing services...")
    for svc in self.services:
      self.services[svc] = self.services[svc]()

    logging.info("Starting webserver...")
    listener = _get_post_handler(self.compile)
    self.socket = _get_socket_listener(self)
    tornado.web.Application([(r"/app-data/(.*)", tornado.web.StaticFileHandler, {"path": "app-data"}), (r"/websocket", self.socket), (r"/.*", listener)]).listen(8080)
    ioloop = tornado.ioloop.IOLoop.current()
    _set_ping(ioloop, timedelta(seconds=2))
    # TODO: This can't be properly stopped on windows, check for fix
    t = threading.Thread(target=ioloop.start)
    t.start()


class View(object):
  """
  The ``View`` abstract class is used to model the structure of a page, as well as the different user actions handled by
  the page. To define views in your application, simply inherit this class and override :meth:`run`.
  """

  title = None
  """
  The title of the view. Will be formatted into ``Application.base_title``
  """

  stylesheet = None
  """
  The stylesheet used for the view.
  """

  def __init__(self, context):
    """
    Constructor of the view

    :param context: Reference to the :class:`Application` instanciating the view.
    :raises NotImplementedError: When ``View.title`` not set in the class definition.
    """

    if self.title is None:
      raise NotImplementedError

    self.document = Document(id="doc", view=self)

    self._head = Head(id="head", parent=self.document)

    self.root = Body(id="body", parent=self.document)
    """
    Instance of :class:`~.widgets.structure.Body`. Root element of the view.
    """

    # TODO: Move this to AST generation, this will allow to get rid of all the hardcoded javascript
    self._js_event_root = "window.onload = function() {{ {code} }};"
    self._server_event_root = 'ws = new WebSocket("ws://localhost:8080/websocket");ws.onopen = function() {{ {code} }};ws.onmessage = HandleMessage;'

    self.ctx = context
    """
    Reference to the :class:`Application` instanciating the view.
    """

    self.server_events = []
    self.evt_handlers = []

    self.socket_events = {}

  def run(self, params=None):
    """
    Build the DOM of the view and registers the events handled by the view.
    This method should tie the whole DOM to ``View.root``.

    :param params: parameters passed to this view
    :raises NotImplementedError: when not overriden in child class
    """
    raise NotImplementedError

  @client
  def HandleMessage(event):
    dat = event.data

    # TODO: impement ast transform from json.loads -> JSON.parse & build js_stl object encapsulating this function
    msg = JSON.parse(dat)

    tId = msg["element_id"]
    evt = msg["event"]
    msgData = None

    if msg.hasOwnProperty("data"):
      msgData = msg["data"]

    targetElem = document.getElementById(tId)

    if evt == "redraw":
      Redraw(targetElem, msgData)

  @client
  def Redraw(target, data):
    target.innerHTML = data["inner_html"]

  def render(self):
    """
    Called by :meth:`~.Application.compile`

    :returns: HTML string representation of the view.
    """

    javascript = {
        "top_level": "",
        "events": "",
        "server_events": ""
    }

    self.document._update_events()
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
    Script(id="main-script", js=final_js, parent=self._head)

    return self.document.compile()

  def on(self, event, control=None, action=None):
    """
    Declare a new event to be handled by the view
    """
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
