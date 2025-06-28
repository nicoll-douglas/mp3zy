# env
from dotenv import load_dotenv
load_dotenv()

# logging
import logging, os

logging.basicConfig(
  level=logging.INFO if os.getenv("APP_ENV") == "production" else logging.DEBUG, 
  format="%(levelname)s | %(message)s"
)

from services import cli