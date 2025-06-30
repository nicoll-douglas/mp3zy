import os, logging
from ftplib import FTP_TLS, error_perm

class FtpClient:
  __FTP_USERNAME = os.getenv("FTP_USERNAME")
  __FTP_PASSWORD = os.getenv("FTP_PASSWORD")
  __FTP_HOST = os.getenv("FTP_HOST")
  __FTP_PORT = int(os.getenv("FTP_PORT"))
  _ftp_instance: FTP_TLS | None

  def __init__(self):
    self._ftp_instance = None
  
  def connect(self):
    ftps = FTP_TLS()

    logging.info(f"Connecting to FTP host {self.__FTP_HOST}...")
    ftps.connect(self.__FTP_HOST, self.__FTP_PORT)

    logging.info("Securing connection...")
    ftps.auth()
    ftps.prot_p()
    
    logging.info("Logging in with configured credentials...")
    ftps.login(self.__FTP_USERNAME, self.__FTP_PASSWORD)

    self._ftp_instance = ftps
    
    logging.info("Successfully connected to FTP host.")
    return self
  
  def quit(self):
    logging.info("Quitting and closing connection to FTP server...")
    self._ftp_instance.quit()
    logging.info("Successfully quit and closed FTP connection.")
    return True

  def log(level: str, msg: str):
    getattr(logging, level)("(FTP) " + msg)

  def write(self, local_path: str, server_path: str,):
    with open(local_path, "rb") as file:
      self._ftp_instance.storbinary(f"STOR {server_path}", file)
    return self

  def rm(self, path: str):
    logging.debug(f"(FTP) Deleting file: {path}")
    self._ftp_instance.delete(path)
    return self

  def mkdir(self, path: str):
    logging.debug(f"(FTP) Creating directory: {path}")
    original_dir = self._ftp_instance.pwd()

    try:
      self._ftp_instance.cwd(path)
      self._ftp_instance.cwd(original_dir)
    except error_perm:
      self._ftp_instance.mkd(path)

    logging.debug("(FTP) Successfully created directory.")
    return self

  def rmdir(self, path: str):
    self._ftp_instance.rmd(
      self._resolve_path(path)
    )
    return self
  
  def ls(self):
    return self._ftp_instance.nlst()
  
  def exists_here(self, file_or_dir_name: str):
    return file_or_dir_name in self.ls()
  
  def mkdir_p(self, path: str):
    self.log("debug", f"Recursively creating directories: {path}")

    parts = path.strip("/").split("/")
    start_from_root = path[0] == "/"
    current_path = "/" if start_from_root else ""
    
    for part in parts:
      current_path += part
      self.mkdir(current_path)
      current_path += "/"

    self.log("debug", "Successfully created directories.")