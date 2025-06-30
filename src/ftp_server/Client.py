import os, logging
from ftplib import FTP_TLS, error_perm

class Client(FTP_TLS):
  __FTP_USERNAME = os.getenv("FTP_USERNAME")
  __FTP_PASSWORD = os.getenv("FTP_PASSWORD")
  __FTP_HOST = os.getenv("FTP_HOST")
  __FTP_PORT = int(os.getenv("FTP_PORT"))
  _FTP_INTERNAL_STORAGE_ROOT: str = "/storage/emulated/0/ftp_data"


  def __init__(self):
    super().__init__()
  
  def connect(self):
    logging.info(f"Connecting to FTP host {self.__FTP_HOST}...")
    super().connect(self.__FTP_HOST, self.__FTP_PORT)

    logging.info("Securing connection...")
    self.auth()
    self.prot_p()
    
    logging.info("Logging in with configured credentials...")
    self.login(self.__FTP_USERNAME, self.__FTP_PASSWORD)
    
    logging.info("Successfully connected to FTP host.")
    return self
  
  def quit(self):
    logging.info("Closing connection to FTP server...")
    super().quit()
    logging.info("Successfully closed FTP connection.")

  def log(self, level: str, msg: str):
    attr = getattr(logging, level)
    attr("(FTP) " + msg)

  def write(self, local_path: str, server_path: str,):
    self.log("debug", f"Writing {local_path} to {server_path}...")
    with open(local_path, "rb") as file:
      self.storbinary(f"STOR {server_path}", file)
    self.log("debug", "Successfully wrote.")
    return self

  def rm(self, path: str):
    self.log("debug", f"Deleting file: {path}")
    self.delete(path)
    self.log("debug", "Successfully deleted.")
    return self

  def mkdir(self, path: str):
    self.log("debug", f"Creating directory: {path}")
    original_dir = self.pwd()

    try:
      self.cwd(path)
      self.cwd(original_dir)
    except error_perm:
      self.mkd(path)

    self.log("debug", "Successfully created directory.")
    return self

  def exists_here(self, file_or_dir_name: str):
    return file_or_dir_name in self.nlst()
  
  def mkdir_p(self, path: str):
    self.log("debug", f"Recursively creating directories: {path}")
    parts = path.strip("/").split("/")
    current_path = ""
    
    for part in parts:
      current_path += part
      self.mkdir(current_path)
      current_path += "/"

    self.log("debug", "Successfully created directories.")