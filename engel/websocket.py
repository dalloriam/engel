import os
import json
import logging
import asyncio

import webbrowser

from collections import defaultdict

from autobahn.asyncio.websocket import WebSocketServerFactory, WebSocketServerProtocol


class EventProcessor(object):

  def __init__(self):
    self.handlers = defaultdict(lambda: defaultdict(lambda: []))

  def register(self, event, callback, selector=None):
    print('Registering: ' + str(event))

    if selector:
      key = str(id(callback))
    else:
      key = '_'

    self.handlers[event][key].append(callback)

    if event not in ('init', 'load', 'close'):
      capture = False
      if selector is None:
        selector = 'html'
        capture = True

      print('Dispatching: ' + str(event))
      self.dispatch({'name': 'subscribe', 'event': event, 'selector': selector, 'capture': capture, 'key': str(id(callback))})

  def unregister(self, event, callback, selector=None):
    if event not in self.handlers:
      return

    if selector is None:
      self.handlers[event]['_'].remove(callback)
    else:
      self.handlers[event].pop(str(id(callback)))

    if event not in ('init', 'load', 'close'):
      self.dispatch({'name': 'unsubscribe', 'event': event, 'selector': selector, 'key': str(id(callback))})

  def dispatch(self, command):
    self.protocol.sendMessage(bytes(json.dumps(command), 'utf-8'), False)

  @asyncio.coroutine
  def process(self, protocol, event):
    self.protocol = protocol
    event_type = event['event']

    if event_type in self.handlers:
      if 'key' in event:
        key = event['key']
        if key in self.handlers[event_type]:
          for handler in self.handlers[event_type][key]:
            if callable(handler):
              command = yield from handler(event, self)

              if command:
                self.dispatch(command)

      for handler in self.handlers[event_type]['_']:
        if callable(handler):
          command = yield from handler(event, self)
          if command:
            self.dispatch(command)


class EventProtocol(WebSocketServerProtocol):

  def onConnect(self, request):
    logging.info("Client connecting: %s" % request.peer)

  def onOpen(self):
    logging.info("WebSocket connection open")

  @asyncio.coroutine
  def onMessage(self, payload, isBinary):
    if isBinary:
      logging.info("Binary message received (NOT SUPPORTED YET): {} bytes".format(len(payload)))
    else:
      logging.info("Text message received: {}".format(payload.decode('utf-8')))
      body = json.loads(payload.decode('utf-8'))
      if 'event' in body:
        yield from self.processor.process(self, body)

  def onClose(self, wasClean, code, reason):
    logging.info("WebSocket connection closed: {}".format(reason))
    exit(0)


class EventServer(object):

  def __init__(self, hostname="localhost", port="8080", processor=None):
    self.hostname = hostname
    self.port = port
    self.processor = processor

    factory = WebSocketServerFactory(u"ws://" + hostname + u":" + str(port))

    protocol = EventProtocol
    protocol.processor = processor
    protocol.app = self

    factory.protocol = protocol

    self.loop = asyncio.get_event_loop()
    self.server = self.loop.create_server(factory, '0.0.0.0', port)

  def start(self, callback=None):
    self.loop.run_until_complete(self.server)

    try:
      path = os.path.dirname(os.path.realpath(__file__))
      webbrowser.open('file:///' + os.path.join(path, 'index.html'))
      self.loop.run_forever()

    except KeyboardInterrupt:
      pass

    finally:
      self.server.close()
      self.loop.close()

      if callback is not None and callable(callback):
        callback()
