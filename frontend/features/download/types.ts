import type { TrackBitrate, TrackCodec, TrackArtistNames } from "@/types";

/**
 * Represents a download search result retrieved from the backend API.
 */
export interface DownloadSearchResult {
  title: string | null;
  channel: string | null;
  url: string;
  duration: number | null;
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
  track_name: string;
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
  artist_names: TrackArtistNames;
  track_name: string;
  album_name: string | null;
  codec: TrackCodec;
  bitrate: TrackBitrate;
  track_number: number | null;
  disc_number: number | null;
  release_date: TrackReleaseDate | null;
  url: string;
  download_dir: string;
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
