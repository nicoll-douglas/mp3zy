import type { TrackBitrate, TrackCodec, TrackArtistNames } from "@/types";

/**
 * Represents a YouTube video search result retrieved from the backend API.
 */
export interface DownloadSearchResult {
  /**
   * The title of the video.
   */
  title: string | null;

  /**
   * The channel of the video.
   */
  channel: string | null;

  /**
   * The webpage URL of the video.
   */
  url: string;

  /**
   * The duration of the video in seconds.
   */
  duration: number | null;

  /**
   * A URL of the video's thumbnail.
   */
  thumbnail: string | null;
}

/**
 * Represents track release date metadata.
 */
export type TrackReleaseDate =
  | {
      year: number;
      month: null;
      day: null;
    }
  | {
      year: number;
      month: number;
      day: number | null;
    };

/**
 * Represents the URL query parameters that must be sent with a downloads search backend API request.
 */
export interface GetDownloadsSearchRequest {
  /**
   * The name of a track.
   */
  track_name: string;

  /**
   * The main artist associated with the track.
   */
  main_artist: string;
}

/**
 * Represents the various reponses that may be returned from a downloads search backend API request.
 */
export type GetDownloadsSearchResponse =
  | {
      status: 200;
      body: {
        results: DownloadSearchResult[];
      };
    }
  | {
      status: 400;
      body: {
        parameter: string;
        message: string;
      };
    }
  | {
      status: 500;
      body: {
        message: string;
      };
    };

/**
 * Represents the request body structure that must be sent with a track download backend API request.
 */
export interface PostDownloadsRequest {
  /**
   * The artist name metadata to use for the track.
   */
  artist_names: TrackArtistNames;

  /**
   * The name of the track.
   */
  track_name: string;

  /**
   * The album name of the track.
   */
  album_name: string | null;

  /**
   * The audio codec to be used for the download.
   */
  codec: TrackCodec;

  /**
   * The audio bitrate to be used for the download.
   */
  bitrate: TrackBitrate;

  /**
   * The track number metadata to use for the track.
   */
  track_number: number | null;

  /**
   * The disc number metadata to use for the track.
   */
  disc_number: number | null;

  /**
   * The release date metadata to use for the track.
   */
  release_date: TrackReleaseDate | null;

  /**
   * The source URL to use for the download.
   */
  url: string;

  /**
   * The target save directory of the download.
   */
  download_dir: string;

  /**
   * A file path to an image file to use for album cover metadata.
   */
  album_cover_path: string | null;
}

/**
 * Represents the various reponses that may be returned from a track download backend API request.
 */
export type PostDownloadsResponse =
  | {
      status: 200;
      body: {
        download_id: number;
        message: string;
      };
    }
  | {
      status: 400;
      body: {
        field: string;
        message: string;
      };
    };
