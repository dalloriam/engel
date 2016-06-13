import json
import tornado.websocket


def get_socket_listener(application):
  class WebSocketListener(tornado.websocket.WebSocketHandler):

    def open(self):
      print("WebSocket Opened.")

    def on_message(self, message):
      # Simply pass event to application
      msg = json.loads(message)
      event = msg["event"]
      elem = msg["element_id"]
      data = msg["data"] if "data" in msg else None

      if data:
        application.current_view.socket_events[event][elem](data)
      else:
        application.current_view.socket_events[event][elem]()

    def send_message(self, message):
      # Send update message to control
      pass

    def close(self):
      print("WebSocket Closed.")

  return WebSocketListener
