from collections import UserDict

class DownloadSearchResult(UserDict):
  def __init__(
    self,
    title: str, 
    channel: str,
    duration: float | int,
    url: str
  ):
    super.__init__()
    self["title"] = title
    self["channel"] = channel
    self["duration"] = duration
    self["url"] = url
  # END __init__

# END class DownloadSearchResult