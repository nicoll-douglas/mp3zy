import logging
import traceback
import sys
import requests

try:
  STARTING_STEP = int(sys.argv[1])
except ValueError:
  logging.critical("Arg 1 must be an integer.")
  sys.exit(1)
except IndexError:
  STARTING_STEP = 0

def attempt(step_name: str, step_handler, step_number: int):
  if step_number >= STARTING_STEP or step_number == 0:
    step_start(step_number, step_name)

    try:
      result = step_handler()
      step_success(step_number)
      return result
    except Exception:
      logging.critical("A critical error occurred:")
      traceback.print_exc()
      step_fail(step_number)
      logging.info("Exiting...")
      sys.exit(1)

def step_start(number: int, name: str):
  logging.info(f"🟡 STEP {number}: {name} 🟡")

def step_fail(number: int):
  logging.info(f"🔴 STEP {number} FAILED 🔴")

def step_success(number: int):
  logging.info(f"🟢 STEP {number} SUCCEEDED 🟢")