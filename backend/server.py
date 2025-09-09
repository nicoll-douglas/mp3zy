from routes import app
from flask_cors import CORS
import os

allowed_origins = [
  os.getenv("VITE_APP_URL"),
  "file://*",
  "app://*"
]

CORS(
  app, 
  resources={r"/*": {"origins": allowed_origins}}
)

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=8888, debug=False)