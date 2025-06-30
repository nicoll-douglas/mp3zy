import bootstrap
from services import FtpClient

client = FtpClient()
client.connect()
client.write("track.mp3", "track.mp3")
client.quit()