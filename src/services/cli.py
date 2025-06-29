import sys, logging

_ARGS = {}

try:
  _ARGS["STARTING_STEP"] = int(sys.argv[1])
except ValueError:
  logging.critical("Arg 1 (workflow step to start from) must be an integer.")
  sys.exit(1)
except IndexError:
  _ARGS["STARTING_STEP"] = 1

def arg(name: str):
  return _ARGS.get(name, None)