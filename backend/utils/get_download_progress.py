def get_download_progress(downloaded_bytes, total_bytes):
  return round(100 * (downloaded_bytes / total_bytes))