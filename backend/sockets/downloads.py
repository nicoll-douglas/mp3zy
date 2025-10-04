from flask_socketio import Namespace

class DownloadsNamespace(Namespace):
  def on_connect(self):
    pass

  def on_disconnect(self):
    pass