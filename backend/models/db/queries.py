def get_downloads(status: bool):
  return f"""
SELECT 
  d.id AS download_id,
  d.url,
  d.codec,
  d.bitrate,
  d.status,
  d.error,
  d.downloaded_bytes,
  d.total_bytes,
  d.speed,
  d.eta,
  d.elapsed,
  d.created_at AS created_at,
  d.updated_at AS updated_at,
  d.completed_at AS completed_at,
  
  -- Metadata fields
  m.track,
  m.album,
  m.track_number,
  m.disc_number,
  m.release_date,
  
  -- Aggregate artist names
  json_group_array(a.name) AS artists

FROM downloads d
JOIN metadata m ON d.metadata_id = m.id
LEFT JOIN metadata_artists ma ON m.id = ma.metadata_id
LEFT JOIN artists a ON ma.artist_id = a.id

{"WHERE d.status = ?" if status else ""}
GROUP BY d.id
"""