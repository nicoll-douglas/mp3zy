class GetDownloadsSearchRequest:
  """Type that represents a validated request body to endpoint GET /downloads/search

  Attributes:
    track_name (str): The name of a track.
    main_artist (str): The name of the main artist associated with the track.
  """
  
  track_name: str
  main_artist: str
  
# END class GetDownloadsSearchRequest
