import json
import logging
import tornado.websocket


def get_socket_listener(application):
  class WebSocketListener(tornado.websocket.WebSocketHandler):

    current_client = None

    def open(self):
      logging.info("WebSocket Opened.")
      WebSocketListener.current_client = self

    def on_message(self, message):
      # Simply pass event to application
      msg = json.loads(message)
      event = msg["event"]
      elem = msg["element_id"]
      data = msg["data"] if "data" in msg else None
      logging.debug("Got WebSocket '{0}' event from {1}".format(event, elem))

      if data:
        application.current_view.socket_events[event][elem](data)
      else:
        application.current_view.socket_events[event][elem]()

    def send_message(self, message):
      # Send update message to control
      pass

    def close(self):
      logging.info("WebSocket Closed.")
      WebSocketListener.current_client = None

  return WebSocketListener
