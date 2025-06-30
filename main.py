from __future__ import annotations
import bootstrap
from services import SpotifyApiClient, SpotifySync

SPOTIFY_CLIENT = SpotifyApiClient()
SPOTIFY_SYNC = SpotifySync(SPOTIFY_CLIENT)

SPOTIFY_SYNC.sync()