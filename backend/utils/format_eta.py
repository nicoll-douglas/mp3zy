def format_eta(seconds: float | int | None) -> str:
  if seconds is None:
    return ""
  
  seconds = int(round(seconds))
  hours, remainder = divmod(seconds, 3600)
  minutes, secs = divmod(remainder, 60)

  if hours > 0:
    return f"{hours:02}:{minutes:02}:{secs:02}"

  return f"{minutes:02}:{secs:02}"
