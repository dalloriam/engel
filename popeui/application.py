"""
Contains all the classes and functions related to the structure of a PopeUI application.
"""
import logging
import asyncio

from .websocket import EventProcessor, EventServer

from .widgets.structure import Body, Document, Head
from .widgets.abstract import PageTitle


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

    self.processor = EventProcessor()
    self.server = EventServer(processor=self.processor)

    if self.base_title is None:
      raise NotImplementedError

    self.services = {}
    self.views = {}
    self.current_view = None

    self.register('init', lambda evt, interface: self.load_view('default'))

  def start(self):
    """
    Start the PopeUI application by initializing all registered services and starting a tornado IOLoop in a seperate thread.
    """
    # TODO: Support params for services by mapping {servicename: {class, params}}?
    for service in self.services.keys():
      self.services[service] = self.services[service]()

    self.server.start()

  def register(self, event, callback, selector=None):
    self.processor.register(event, callback, selector)

  def unregister(self, event, callback, selector=None):
    self.processor.unregister(event, callback, selector)

  def dispatch(self, command):
    self.processor.dispatch(command)

  @asyncio.coroutine
  def load_view(self, view_name):
    if view_name not in self.views:
      raise NotImplementedError
    self.current_view = self.views[view_name](self)
    return self.current_view.render()


class View(object):

  title = None

  libraries = []

  def __init__(self, context):

    if self.title is None:
      raise NotImplementedError
    self.is_loaded = False
    self._doc_root = Document(id="popeui-main", view=self)
    self._head = Head(id="popeui-head", parent=self._doc_root)
    self.root = Body(id="main-body", parent=self._doc_root)
    self.context = context

    for library in self.libraries:
      print("Loading library...")
      for stylesheet in library.stylesheets:
        self._head.load_stylesheet(id(stylesheet), stylesheet)
      for script in library.scripts:
        self._head.load_script(id(script), script)

    self._event_cache = []

    self.context.register('load', self._unpack_events)

  def build(self):
    raise NotImplementedError

  def on(self, event, callback, selector=None):
    self._event_cache.append({'event': event, 'callback': asyncio.coroutine(callback), 'selector': selector})

  def dispatch(self, command):
    self.context.dispatch(command)

  @asyncio.coroutine
  def _unpack_events(self, event, interface):
    self.is_loaded = True
    for evt in self._event_cache:
      self.context.register(evt['event'], evt['callback'], evt['selector'])

  def render(self):
    PageTitle(id="_page-title", text=self.context.base_title.format(self.title), parent=self._head)
    self.build()
    return {'name': 'init', 'html': self._doc_root.compile()}
