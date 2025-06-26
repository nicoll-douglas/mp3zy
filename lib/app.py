from . import logger
import traceback
import sys

# attempt a step in the script
def attempt(name, handler, step_number):
  if step_number >= get_starting_step():
    logger.step_start(step_number, name)

    try:
      handler()
    except Exception:
      logger.error("An error ocurred:")
      traceback.print_exc()
      logger.step_fail(step_number)
      logger.debug("\nExiting...")
      sys.exit(1)

    logger.step_success(step_number)

# get the step from which to start from
def get_starting_step():
  try:
    return int(sys.argv[1])
  except ValueError:
    logger.error("Arg 1 must be an integer.")
    sys.exit(1)
  