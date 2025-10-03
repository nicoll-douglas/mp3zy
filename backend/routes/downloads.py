from flask import Blueprint, request, jsonify
import request_validate, models, db
from typing import cast
from user_types.reponses import PostDownloadsResponse
from user_types.requests import PostDownloadsRequest
from services import Downloader

downloads_bp = Blueprint("downloads", __name__)

@downloads_bp.route("/downloads", methods=["POST"])
def post_downloads():
  data = request.get_json()
  is_valid, validation_result_data = request_validate.post_downloads_validate(data)

  if not is_valid:
    res_body = cast(PostDownloadsResponse.BadRequest, validation_result_data)
    return jsonify(res_body.__dict__), 400
  
  req_body = cast(PostDownloadsRequest, validation_result_data)
  
  with db.connect() as conn:
    artist_ids = models.db.Artist(conn).insert_many([
      { "name": n } 
      for n in req_body.artist_names
    ])

    metadata_id = models.db.Metadata(conn).insert({
      "track_name": req_body.track_name,
      "album_name": req_body.album_name,
      "track_number": req_body.track_number,
      "disc_number": req_body.disc_number,
      "release_date": str(req_body.release_date)
    })
    metadata_id = cast(int, metadata_id)

    models.db.MetadataArtist(conn).insert_many([
      { "metadata_id": metadata_id, "artist_id": aid }
      for aid in artist_ids
    ])

    download_id = models.db.Download(conn).insert_as_queued({
      "url": req_body.url,
      "codec": req_body.codec.value,
      "bitrate": req_body.bitrate.value,
      "metadata_id": metadata_id
    })

  Downloader.start()
  
  return jsonify(PostDownloadsResponse.Ok(download_id).__dict__)
# END post_downloads