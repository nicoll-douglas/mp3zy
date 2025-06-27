from . import logger
import traceback
import sys
import requests

try:
  STARTING_STEP = int(sys.argv[1])
except ValueError:
  logger.error("Arg 1 must be an integer.")
  sys.exit(1)

# attempt a step in the script
def attempt(name: str, handler, step_number: int):
  if step_number >= STARTING_STEP or step_number == 0:
    logger.step_start(step_number, name)

    try:
      handler()
    except Exception:
      logger.error("An error occurred:")
      traceback.print_exc()
      logger.step_fail(step_number)
      logger.debug("Exiting...")
      sys.exit(1)

    logger.step_success(step_number)

def handle_http_response(response: requests.Response, request_name: str | None):
  if response.status_code != 200:
    raise RuntimeError(f"{request_name or "Request"} failed with status code {response.status_code}.\nResponse body:\n{response.text}")
  else:
    logger.success(f"{request_name or "Request"} succeeded.")