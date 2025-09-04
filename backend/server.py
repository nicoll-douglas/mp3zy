from routes import app
from flask_cors import CORS

allowed_origins = [
  "http://127.0.0.1:5173",
  "file://*",
  "app://*"
]

CORS(
  app, 
  resources={r"/*": {"origins": allowed_origins}}
)

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=8888, debug=False)