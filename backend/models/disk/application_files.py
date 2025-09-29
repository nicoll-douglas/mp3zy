import os, json
from platformdirs import user_cache_dir

class ApplicationFiles:
  SETTINGS_LOCATION: str = os.path.join(os.getenv("DATA_DIR"), "settings.json")
  CACHE_DIR: str = user_cache_dir(os.getenv("VITE_APP_NAME"))


  @classmethod
  def load_settings(cls):
    with open(cls.SETTINGS_LOCATION, "r") as file:
      return json.load(file)
    
  @classmethod
  def save_path(cls):
    settings = cls.load_settings()
    return settings["savePath"]

  @classmethod
  def collections_parent_dir(cls):
    return os.path.join(cls.save_path(), "collections")
  
  @classmethod
  def collection_dir(cls, codec):
    return os.path.join(cls.collections_parent_dir(), codec)
  
  @classmethod
  def covers_dir(cls):
    return os.path.join(cls.CACHE_DIR, "covers")