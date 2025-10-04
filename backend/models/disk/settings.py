import os, json

class Settings:
  FILE_LOCATION: str = os.path.join(os.getenv("USER_DATA_DIR"), "settings.json")

  @classmethod
  def load_settings(cls):
    with open(cls.FILE_LOCATION, "r", encoding="utf-8") as file:
      return json.load(file)