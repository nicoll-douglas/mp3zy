import os
from platformdirs import user_cache_dir

class Cache:
  """A model class for interfacing with the application cache.

  Attributes:
    DIR (str): The path of the cache directory.
  """

  DIR = user_cache_dir(os.getenv("APP_NAME"))

# END class Cache