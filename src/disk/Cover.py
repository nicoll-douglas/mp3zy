from __future__ import annotations
from disk.File import File

class Cover(File):
  DIR: str | None
  _source: str | None

  def __init__(
    self, 
    _id: str | None = None,
    ext: str | None = None, 
    source: str | None = None, 
    path: str | None = None,
    _dir: str | None = None
  ):
    self._source = source
    if _dir:
      self.DIR = _dir

    if not _id and self._source:
      _id = self._source.split("/")[-1]

    super().__init__(
      _id=_id,
      ext=ext,
      path=path
    )
