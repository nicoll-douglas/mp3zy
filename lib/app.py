from . import logger
import traceback
import sys

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