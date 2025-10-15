import os

# the CORS origins allowed to access the Flask app
CORS_ALLOWED_ORIGINS = [
  "file://*",
  "app://*"
]

frontend_app_url = os.getenv("FRONTEND_APP_URL")

if frontend_app_url:
  CORS_ALLOWED_ORIGINS.append(frontend_app_url)