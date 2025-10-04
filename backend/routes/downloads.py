from flask import Blueprint, request, jsonify, Response
import request_validate as reqv
from typing import cast, Literal
from user_types.reponses import PostDownloadsResponse, GetDownloadsSearchResponse
from user_types.requests import PostDownloadsRequest, GetDownloadsSearchRequest
from services import Downloader, YtDlpClient

downloads_bp = Blueprint("downloads", __name__)

@downloads_bp.route("/downloads", methods=["POST"])
def post_downloads() -> tuple[Response, Literal[400, 200]]:
  """Adds a track to the download queue for the downloader thread to pick up and download.
  
  Returns:
    tuple[Response, Literal[400, 200]]: The response and status code.
  """

  data = request.get_json()
  is_valid, validation_result_data = reqv.post_downloads_validate(data)

  if not is_valid:
    res_body = cast(PostDownloadsResponse.BadRequest, validation_result_data)
    return jsonify(res_body.__dict__), 400
  
  req_body = cast(PostDownloadsRequest, validation_result_data)
  download_id = Downloader.queue(req_body)

  Downloader.start()
  
  return jsonify(PostDownloadsResponse.Ok(download_id).__dict__), 200
# END post_downloads


@downloads_bp.route("/downloads/search", methods=["GET"])
def get_downloads_search():
  """Interfaces with yt-dlp to query for search results of YouTube videos to be downloaded.
  
  Returns:
    tuple[Response, Literal[400, 200]]: The response and status code.
  """

  is_valid, validation_result_data = reqv.get_downloads_search_validate(request.args)

  if not is_valid:
    res_body = cast(GetDownloadsSearchResponse.BadRequest, validation_result_data)
    return jsonify(res_body.__dict__), 400

  req_body = cast(GetDownloadsSearchRequest, validation_result_data)
  search_results = YtDlpClient().query_youtube(req_body)
      
  return jsonify(GetDownloadsSearchResponse.Ok(search_results).get_serializable()), 200
# END get_downloads_search