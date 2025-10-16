from flask import Blueprint, request, jsonify, Response
import request_validate as reqv
from typing import cast, Literal
import user_types.reponses as res
import user_types.requests as req
from user_types import DownloadSearchResult
from services import Downloader, YtDlpClient

downloads_bp = Blueprint("downloads", __name__)

@downloads_bp.route("/downloads", methods=["POST"])
def post_downloads() -> tuple[Response, Literal[400, 200]]:
  """Adds a track to the download queue for the downloader thread to pick up and download.
  
  Returns:
    tuple[Response, Literal[400, 200]]: The response and status code.
  """

  raw_body = request.get_json()
  is_valid, validation_result_data = reqv.PostDownloadsValidator().validate(raw_body)

  if not is_valid:
    res_body = cast(res.PostDownloadsResponse.BadRequest, validation_result_data)
    return jsonify(res_body.__dict__), 400
  
  req_body = cast(res.PostDownloadsRequest, validation_result_data)
  res_body = res.PostDownloadsResponse.Ok()
  res_body.download_id = Downloader.queue(req_body)

  Downloader.start()
  
  return jsonify(res_body.__dict__), 200
# END post_downloads


@downloads_bp.route("/downloads/search", methods=["GET"])
def get_downloads_search():
  """Interfaces with yt-dlp to query for search results of YouTube videos to be downloaded.
  
  Returns:
    tuple[Response, Literal[400, 500, 200]]: The response and status code.
  """

  is_valid, validation_result_data = reqv.GetDownloadsSearchValidator().validate(request.args)

  if not is_valid:
    res_body = cast(res.GetDownloadsSearchResponse.BadRequest, validation_result_data)
    return jsonify(res_body.__dict__), 400

  req_body = cast(req.GetDownloadsSearchRequest, validation_result_data)
  is_success, result = YtDlpClient().query_youtube(req_body)

  if not is_success:
    res_body = res.GetDownloadsSearchResponse.ServerError()
    res_body.message = cast(str, result)
    return jsonify(res_body.__dict__), 500

  res_body = res.GetDownloadsSearchResponse.Ok()
  res_body.results = cast(list[DownloadSearchResult], result)
  
  return jsonify(res_body.get_serializable()), 200
# END get_downloads_search

@downloads_bp.route("/downloads/restart", methods=["POST"])
def post_downloads_restart():
  """Sets a track to queued for the downloader thread to pick up and restart the download.
  
  Returns:
    tuple[Response, Literal[400, 200, 500]]: The response and status code.
  """

  raw_body = request.get_json()
  is_valid, validation_result_data = reqv.PostDownloadsRestartValidator().validate(raw_body)

  if not is_valid:
    res_body = cast(res.PostDownloadsResponse.BadRequest, validation_result_data)
    return jsonify(res_body.__dict__), 400

  req_body = cast(req.PostDownloadsRestartRequest, validation_result_data)
  requeud = Downloader.requeue(req_body)

  if not requeud:
    res_body = res.PostDownloadsRestartResponse.ServerError()
    res_body.message = "Failed to restart download, the download may already be in progress or does not exist."

    return jsonify(res_body.__dict__), 500
  
  Downloader.start()
  
  res_body = res.PostDownloadsRestartResponse.Ok()

  return jsonify(res_body.__dict__), 200
# END post_downloads_restart