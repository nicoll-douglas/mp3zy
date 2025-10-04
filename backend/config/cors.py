import os

CORS_ALLOWED_ORIGINS = [
  os.getenv("VITE_APP_URL"),
  "file://*",
  "app://*"
]