from flask import Blueprint, request, jsonify, Response
import request_validate, models, db
from typing import cast, Literal
from user_types.reponses import PostDownloadsResponse
from user_types.requests import PostDownloadsRequest
from services import Downloader

downloads_bp = Blueprint("downloads", __name__)

@downloads_bp.route("/downloads", methods=["POST"])
def post_downloads() -> tuple[Response, Literal[400, 200]]:
  """Adds a track to the download queue for the downloader thread to pick up and download.
  
  Returns:
    tuple[Response, Literal[400, 200]]: The response and status code.
  """

  data = request.get_json()
  is_valid, validation_result_data = request_validate.post_downloads_validate(data)

  if not is_valid:
    res_body = cast(PostDownloadsResponse.BadRequest, validation_result_data)
    return jsonify(res_body.__dict__), 400
  
  req_body = cast(PostDownloadsRequest, validation_result_data)
  download_id = Downloader.queue(req_body)

  Downloader.start()
  
  return jsonify(PostDownloadsResponse.Ok(download_id).__dict__), 200
# END post_downloads