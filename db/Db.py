import logging
import sqlite3

class Db:
  __LOCATION = "db/app.db"
  __SCHEMA = "db/schema.sql"

  def connect(self):
    logging.info(f"Connecting to database `{self.__LOCATION}`")
    conn = sqlite3.connect(self.__LOCATION)
    logging.info(f"Successfully connected to database.")
    return conn

  def setup(self, conn: sqlite3.Connection):
    logging.info("Setting up database.")

    logging.debug("Creating tables...")
    with open(self.__SCHEMA, "r") as file:
      schema_script = file.read()
    
    cursor = conn.cursor()
    cursor.executescript(schema_script)
    conn.commit()
    logging.debug("Finished creating tables.")

    logging.info("Finished setting up database.")
