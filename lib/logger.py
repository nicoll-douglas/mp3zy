def error(message: str):
  print(f"❌ {message}")

def success(message: str):
  print(f"✅ {message}")

def debug(message: str):
  print(f"⚒️ {message}")

def info(message: str):
  print(f"ℹ️  {message}")

def step_start(number: int, name: str):
  print(f"🟡 STEP {number}: {name} 🟡")

def step_fail(number: int):
  print(f"🔴 STEP {number} FAILED 🔴\n")

def step_success(number: int):
  print(f"🟢 STEP {number} SUCCEEDED 🟢\n")