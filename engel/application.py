"""
Contains all the classes and functions related to the structure of an Engel application.
"""
import logging
import asyncio

from .websocket import EventProcessor, EventServer

from .widgets.structure import Body, Document, Head
from .widgets.abstract import PageTitle


class Application(object):
  """
  The ``Application`` abstract class represents the entirety of an Engel application.

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

    self.register('init', lambda evt, interface: self._load_view('default'))

  def start(self, on_exit_callback=None):
    """
    Start the Engel application by initializing all registered services and starting an Autobahn IOLoop.

    :param on_exit_callback: Callback triggered on application exit
    """
    # TODO: Support params for services by mapping {servicename: {class, params}}?
    for service in self.services.keys():
      self.services[service] = self.services[service]()

    self.server.start(on_exit_callback)

  def register(self, event, callback, selector=None):
    """
    Resister an event that you want to monitor.

    :param event: Name of the event to monitor
    :param callback: Callback function for when the event is received (Params: event, interface).
    :param selector: `(Optional)` CSS selector for the element(s) you want to monitor.
    """
    self.processor.register(event, callback, selector)

  def unregister(self, event, callback, selector=None):
    """
    Unregisters an event that was being monitored.

    :param event: Name of the event to monitor
    :param callback: Callback function for when the event is received (Params: event, interface).
    :param selector: `(Optional)` CSS selector for the element(s) you want to monitor
    """
    self.processor.unregister(event, callback, selector)

  def dispatch(self, command):
    """
    Method used for sending events to the client. Refer to ``engel/engeljs.js`` to see the events supported by the client.

    :param command: Command dict to send to the client.
    """
    self.processor.dispatch(command)

  @asyncio.coroutine
  def _load_view(self, view_name):
    if view_name not in self.views:
      raise NotImplementedError
    if self.current_view is not None:
      self.current_view.unload()
    self.current_view = self.views[view_name](self)
    return self.current_view._render()


class View(object):

  title = None
  """
  Title of the view.
  """

  stylesheet = None
  """
  Stylesheet of the view.
  """

  libraries = []
  """
  List of modules encapsulating the javascript libraries used by the view.
  """

  def __init__(self, context):
    """
    Constructor of the view.

    :param context: Application instantiating the view.
    :raises NotImplementedError: When ``View.title`` is not set.
    """

    if self.title is None:
      raise NotImplementedError

    self.is_loaded = False
    self._doc_root = Document(id="engel-main", view=self)
    self._head = Head(id="engel-head", parent=self._doc_root)
    self.root = Body(id="main-body", parent=self._doc_root)
    self.context = context

    for library in self.libraries:
      print("Loading library...")
      for stylesheet in library.stylesheets:
        self._head.load_stylesheet(id(stylesheet), stylesheet)
      for script in library.scripts:
        self._head.load_script(id(script), script)

    if self.stylesheet is not None:
      self._head.load_stylesheet('main-stylesheet', self.stylesheet)

    self._event_cache = []

    self.context.register('load', self._unpack_events)

  def build(self):
    """
    Method building the layout of the view. Override this in your view subclass to define your view's layout.
    """
    raise NotImplementedError

  def on(self, event, callback, selector=None):
    """
    Wrapper around :meth:`~.application.Application.register`. If :meth:`~.application.View.on` is called, for instance, during :meth:`~.application.View.build`,
    the event handlers will be enqueued and registered when the view is loaded. Similarly, if :meth:`~.application.View.on` is called once the view is loaded (for example, in a button callback),
    the event handler will be registered immediately.

    :param event: Name of the event to monitor
    :param callback: Callback function for when the event is received (Params: event, interface).
    :param selector: `(Optional)` CSS selector for the element(s) you want to monitor
    """
    cbk = asyncio.coroutine(callback)
    self._event_cache.append({'event': event, 'callback': cbk, 'selector': selector})
    if self.is_loaded:
      self.context.register(event, cbk, selector)

  def dispatch(self, command):
    """
    Dispatch a command to the client at view-level.

    :param command: Command dict to send to the client.
    """
    self.context.dispatch(command)

  @asyncio.coroutine
  def _unpack_events(self, event, interface):
    self.is_loaded = True
    for evt in self._event_cache:
      self.context.register(evt['event'], evt['callback'], evt['selector'])

  def unload(self):
    """
    Overridable method called when a view is unloaded (either on view change or on application shutdown).
    Handles by default the unregistering of all event handlers previously registered by
    the view.
    """
    self.is_loaded = False
    for evt in self._event_cache:
      self.context.unregister(evt['event'], evt['callback'], evt['selector'])
    self._event_cache = {}

  def _render(self):
    PageTitle(id="_page-title", text=self.context.base_title.format(self.title), parent=self._head)
    self.build()
    return {'name': 'init', 'html': self._doc_root.compile()}
