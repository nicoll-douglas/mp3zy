from disk import Playlist

def store_playlist(pl_name, pl_items):
  print(f"Creating playlist file for playlist '{pl_name}'...")
  p = Playlist(
    name=pl_name,
    directory=Playlist.DESKTOP_PL_DIR
  )
  p.path = p.build_path()
  p.write(pl_items)
  print("✅ Playlist file created.")