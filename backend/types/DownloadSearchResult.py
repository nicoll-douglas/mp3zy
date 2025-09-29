from collections import UserDict

class DownloadSearchResult(UserDict):
  def __init__(
    self,
    title: str, 
    channel: str,
    duration: float | int,
    url: str
  ):
    self["title"] = title
    self["channel"] = channel
    self["duration"] = duration
    self["url"] = url
