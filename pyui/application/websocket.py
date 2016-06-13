import tornado.websocket


def get_socket_listener(application):
  class WebSocketListener(tornado.websocket.WebSocketHandler):

    def open(self):
      print("WebSocket Opened.")

    def on_message(self, message):
      # message = {control_id: "123", event: "123", data: {[...]}}
      # Simply pass event to application
      pass

    def send_message(self, message):
      # Send update message to control
      pass

    def close(self):
      print("WebSocket Closed.")

  return WebSocketListener
