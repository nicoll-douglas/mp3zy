# mp3zy API v1

Specification for v1 of the mp3zy app's desktop web API.

## Table of Contents

- [Overview](#overview)
- [Type Reference](#type-reference)
  - [TrackBitrate](#trackbitrate)
  - [TrackCodec](#trackcodec)
  - [TrackReleaseDate](#trackreleasedate)
  - [DownloadSearchResult](#downloadsearchresult)
  - [DownloadStatus](#downloadstatus)
  - [DownloadUpdate](#downloadupdate)
- [REST API](#rest-api-1)
  - [POST /downloads](#post-downloads)
  - [GET /downloads/search](#get-downloadssearch)
  - [POST /downloads/restart](#post-downloadsrestart)
  - [DELETE /downloads](#delete-downloads)
  - [DELETE /downloads/{id}](#delete-downloadsid)
  - [GET /metadata](#get-metadata)
  - [GET /spotify-sync/auth-url](#get-spotify-syncauth-url)
  - [POST /spotify-sync/authorize](#post-spotify-syncauthorize)
- [Real-time API](#real-time-api-1)
  - [/downloads](#downloads)

## Overview

### REST API

One part of the mp3zy API consists of a REST API. All requests and responses to these REST endpoints can be expected to be in JSON format.

###

### Real-time API

The other part of the mp3zy API consists of a real-time API for download progress updates using WebSockets and JSON messages.

## Type Reference

### TrackArtistNames

_string[]_

A string array of artist names associated with the track. The array should be of at least length 1:

```
[string, ...string[]]
```

### TrackBitrate

_number_

The possible bitrates that the user can select for a download:

```
128 | 192 | 256;
```

### TrackCodec

_string_

The possible audio codecs that the user can select for a download:

```
"mp3" | "flac";
```

### TrackReleaseDate

_object_

The release date metadata that the user can send for their download.

```
{ "year": number, "month": null, "day": null }
  | { "year": number, "month": number, "day": null }
  | { "year": number, "month": number, "day": number; };
```

- `year` - The year of the release. Should always be present as a _number_.
- `month` - The month of the release. Is either _null_ or _number_.
- `day` - The day of the release. Should always be _null_ if _month_ is _null_, otherwise can be _null_ or _number_.

#### Examples:

```
{
  "year": 2025,
  "month": 9,
  "day": null
}
```

```
{
  "year": 2023,
  "month": null,
  "day": null
}
```

### DownloadSearchResult

_object_

A search result containing basic metadata about a downloadable video from YouTube.

```
{
  "title": string | null,
  "channel": string | null,
  "url": string,
  "duration": number | null,
  "thumbnail: string | null
}
```

- `title` - The video title.
- `channel` - The video's channel/uploader.
- `url` - The URL of the video which can and should be provided for when downloading.
- `duration` - The duration of the video in seconds.
- `thumbnail` - The URL of the video thumbnail.

### DownloadStatus

_string_

The state of a download.

```
"downloading" | "failed" | "queued" | "completed";
```

### DownloadUpdate

_object_

An object containing information about a download update for a track being downloaded.

```
{
  "download_id": number,
  "status": DownloadStatus,
  "downloaded_bytes": number | null,
  "total_bytes": number | null,
  "speed": number | null,
  "eta": number | null,
  "artist_names": TrackArtistNames,
  "track_name": string,
  "codec": TrackCodec,
  "bitrate": TrackBitrate,
  "url": string,
  "created_at": string,
  "terminated_at": string | null,
  "download_dir": string,
  "error_msg": string | null
}
```

- `download_id` - The ID associated with a download record.
- `status` - The current status of the download.
- `downloaded_bytes` - The number of bytes already downloaded if the download was started.
- `total_bytes` - The total number of bytes that is being downloaded if the download was started.
- `speed` - The current speed of the download in bytes per second if the download was started.
- `eta` - The ETA of the download (estimated time until it completes) in seconds if the download was started.
- `artist_names` - The names of the artists associated with the track being downloaded.
- `track_name` - The name of the track being downloaded.
- `codec` - The audio codec of the final file that will be output by the download.
- `bitrate` - The bitrate of the final file that will be output by the download if applicable.
- `url` - The source URL of the file being downloaded.
- `created_at` - A timestamp indicating when the download record was created.
- `terminated_at` - A timestamp indicating when the download completed or failed if so.
- `download_dir` - The directory where the download will be saved to.
- `error_msg` - An error message if the download failed.

## REST API

### POST /downloads

This endpoint will trigger an audio file download of a song from the provided URL.

#### Request

##### Body

```
{
  "artist_names": TrackArtistNames,
  "track_name": string,
  "album_name": string | null,
  "codec": TrackCodec,
  "bitrate": TrackBitrate,
  "track_number": number | null,
  "disc_number": number | null,
  "release_date": TrackReleaseDate | null,
  "url": string,
  "download_dir": string,
  "album_cover_path": string | null
}
```

- `artist_names` - An array of strings of the artists of the track.
- `track_name` - The name of the track/song.
- `album_name` - The name of the track's album.
- `codec` - The audio codec to use when saving the file to disk.
- `bitrate` - The bitrate to use when saving the audio file to disk.
- `track_number` - The number of the track on its disc on the album.
- `disc_number` - The disc number that the track is on on the album.
- `release_date` - The release date of the track.
- `url` - The URL source to use for download (should ideally be extracted from the response body of a request to GET /downloads/search).
- `download_dir` - The directory where the associated audio file should be saved to.
- `album_cover_path` - The path to an image file to be used as album cover metadata.

#### Responses

##### 400

A 400 status will be returned if validation fails (the request body format is not matched) along with the following response body:

```
{
  "field": string,
  "message": string
}
```

- `field` - The first field that failed validation that caused the download to fail. Will match a key in the request body.
- `message` - A user-friendly message indicating why the download failed.

##### 200

The API will return a status code of 200 if the download successfully started along with the following response body:

```
{
  "message": string,
  "download_id": number
}
```

- `message` - A user-friendly message explaining that the download started.
- `download_id` - An ID associated with the download.

### GET /downloads/search

This endpoint retrieves YouTube search results for tracks/songs that may be downloaded, returning basic metadata.

#### Request

##### Parameters

- `track_name` (required) - The name of the track you wish to search for.
- `main_artist` (required) - The name of the primary artist of the track.

#### Responses

##### 400

A 400 status will be returned if either the `track_name` or `main_artist` parameter is missing along with the following response body:

```
{
  "parameter": string,
  "message": string
}
```

- `parameter` - The first parameter that was found to be missing. Will match one of the parameter names.
- `message` - A user-friendly message indicating why the search failed.

##### 500

The API will return a status code of 500 if a server-side error occur preventing the search along with the following response body:

```
{
  "message": string
}
```

- `message` - A user-friendly message indicating the error that occurred.

##### 200

The API will return a status code of 200 if the search was successful along with the following response body:

```
{
  "results": DownloadSearchResult[]
}
```

- `results` - An array of search results, describing the videos that were found.

### POST /downloads/restart

This endpoint will restart a failed download.

#### Request

##### Body

```
{
  "download_id": number
}
```

- `download_id` - A _number_ which is the ID of the download to restart.

#### Responses

##### 400

A 400 status will be returned if validation fails (the request body format is not matched) along with the following response body:

```
{
  "field": string,
  "message": string
}
```

- `field` - The first field that failed validation that caused the download restart attempt to fail. Will match a key in the request body.
- `message` - A user-friendly message indicating why the download failed to restart.

##### 200

The API will return a status code of 200 if the download successfully restarted along with the following response body:

```
{
  "message": string
}
```

- `message` - A user-friendly message explaining that the download restarted.

### DELETE /downloads

Deletes download records.

#### Request

##### Parameters

- `status` (optional) - Only delete downloads with this status (see [DownloadStatus](#downloadstatus))

#### Responses

##### 200

The API will return a status code of 200 if the target records were successfully deleted along with the following response body:

```
{
  "message": string,
  "delete_count": number
}
```

- `message` - A user-friendly message indicating that deletion was a success.
- `delete_count` - A _number_ indicating the amount of records that were deleted.

### DELETE /downloads/{id}

Deletes a download by ID.

#### Request

##### Parameters

- `{id}` - The ID of the download.

#### Responses

#### 400

The API will return a 400 status code if the `{id}` parameter is invalid along with the following response body:

```
{
  "message": string
}
```

- `message` - A user-friendly message indicating that ID is invalid.

##### 404

The API will return a 404 status code if the record attempting to be deleted was not found along with the following response body:

```
{
  "message": string
}
```

- `message` - A user-friendly message indicating that the record was not found.

#### 200

The API will return a 200 status code if the record was successfully deleted along with the following response body:

```
{
  message: string
}
```

- `message` - A user-friendly message indcating that the record was successfully deleted.

### GET /metadata

Queries the Spotify API for track metadata returning only the necessary fields for the application.

#### Request

##### Parameters

- `artist_name` (required) - The artist name associated with the track.
- `track_name` (required) - The name of the track.

#### Responses

##### 401

The API will return a 401 response if the it is not authenticated to make requests to the Spotify API along with the following response body:

```
{
  message: string
}
```

- `message` - A user-friendly message indicating that there is no authorization.

##### 200

The API will return a 200 response on success along with the following response body:

```
{
  "artist_names": string[],
  "track_name": string,
  "album_name": string,
  "track_number": number,
  "disc_number": number,
  "release_date": TrackReleaseDate
}
```

- `artist_names` - The names of the artists associated with the track retrieved from the Spotify API.
- `track_name` - The full name of the track retrieved from the Spotify API.
- `album_name` - The name ofthe album that the track is on.
- `track_number` The track number on the disc on the album of the track.
- `disc_number` - The disc number on the album that the track is on.
- `release_date` - The release date of the track.

### GET /spotify-sync/auth-url

Get an auth URL for the user to click and authorize Spotify account access.

#### Responses

##### 200

The API will return a 200 status code on success along with the following response body:

```
{
  "auth_url": string
}
```

- `auth_url` - The auth URL.

### POST /spotify-sync/authorize

Send an authorization code in order to exchange for an access token and refresh token with the Spotify API.

#### Request

##### Body

```
{
  "auth_code": string
}
```

- `auth_code` - An authorization obtained from a future redirect once the user clicks an auth URL and authenticates with Spotify.

#### Responses

##### 200

The API will return a 200 status code on success along with the following response body:

```
{
  "message": string
}
```

- `message` - A user-friendly message indicating that an access token and refresh token were successfully obtained.

## Real-time API

### /downloads

#### Client-sent Event: `get_downloads`

Subscribes to live updates about the current state of downloads in the application.

##### Client to Server

No payload needs to be sent.

##### Server to Client

The payload will include live updates about downloads in the format below. The initial payload will contain data about all downloads of all statuses and then subsequent payloads will only include incremental updates about any reactive changes to updates i.e status changes, progress changes.

```
DownloadUpdate[]
```

For example, initially we may receive the following payload on the client which includes data about a track currently being downloaded and a previous failed download:

```
[
  {
    "download_id": 1,
    "old_status": null,
    "status": "failed",
    "downloaded_bytes": 2445143,
    "total_bytes": 5932894,
    "speed": 218054.09873454241,
    "eta": 4,
    "artist_names": ["Daft Punk"],
    "track": "Around the World",
    "codec": "mp3",
    "bitrate": 320,
    "url": "https://www.youtube.com/watch?v=dwDns8x3Jb4",
    "created_at": "2025-09-27 22:08:01",
    "completed_at": null,
    "failed_at": "2025-09-27 22:08:07"
  },
  {
    "download_id": 1,
    "old_status": null,
    "status": "downloading",
    "downloaded_bytes": 5203235,
    "total_bytes": 5221585,
    "speed": 210754.56577849746,
    "eta": 1,
    "artist_names": ["Daft Punk"],
    "track": "One More Time",
    "codec": "mp3",
    "bitrate": 320,
    "url": "https://www.youtube.com/watch?v=A2VpR8HahKc",
    "created_at": "2025-09-27 22:08:12",
    "completed_at": null,
    "failed_at": null
  }
]
```

Then on the next update, we may get the following payload only containing data about the track that was being downloaded which has now completed:

```
[
  {
    "download_id": 1,
    "old_status": "downloading",
    "status": "completed",
    "downloaded_bytes": 5221585,
    "total_bytes": 5221585,
    "speed": 210754.56577849746,
    "eta": 1,
    "artist_names": ["Daft Punk"],
    "track": "One More Time",
    "codec": "mp3",
    "bitrate": "320",
    "url": "https://www.youtube.com/watch?v=A2VpR8HahKc",
    "created_at": "2025-09-27 22:08:12",
    "completed_at": "2025-09-27 22:08:15",
    "failed_at": null
  }
]
```

Data about the failed update would not be included in this update and subsequent updates since it would not have many or any reactive changes, unless the download was say for example, retried.
