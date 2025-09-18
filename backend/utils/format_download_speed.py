def format_download_speed(bytes_per_sec: float | int):
  kb = bytes_per_sec / 1024
  mb = bytes_per_sec / (1024 * 1024)

  if mb >= 1:
    return f"{mb:.1f} MB/s"

  return f"{kb:.1f} kB/s"
