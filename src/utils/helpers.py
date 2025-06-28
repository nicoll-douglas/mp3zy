from services import cli
import logging, traceback, sys

def attempt_step(step_details: tuple, step_handler):
  (step_name, step_number) = step_details

  if step_number >= cli.arg("STARTING_STEP") or step_number == 1:
    logging.info(f"🟡 STEP {step_number}: {step_name} 🟡")

    try:
      result = step_handler()
      logging.info(f"🟢 STEP {step_number} SUCCEEDED 🟢")
      return result
    except Exception:
      logging.critical("A critical error occurred:")
      traceback.print_exc()
      logging.critical(f"🔴 STEP {step_number} FAILED 🔴")
      logging.info("Exiting...")
      sys.exit(1)

