import type { TrackCodec, TrackBitrate, TrackArtistNames } from "@/types";

/**
 * Represents the possible statuses that a download can be in.
 */
export type DownloadStatus = "failed" | "downloading" | "completed" | "queued";

/**
 * A download update pertaining to data that may be received from the backend real-time API about a download.
 */
export interface DownloadUpdate {
  /**
   * The ID of the download.
   */
  download_id: number;

  /**
   * The status of the download
   */
  status: DownloadStatus;

  /**
   * The artist name metadata associated with the track.
   */
  artist_names: TrackArtistNames;

  /**
   * The name of the track.
   */
  track_name: string;

  /**
   * The audio codec of the download.
   */
  codec: TrackCodec;

  /**
   * The bitrate of the download.
   */
  bitrate: TrackBitrate;

  /**
   * The source URL used for the download.
   */
  url: string;

  /**
   * The target save directory of the download.
   */
  download_dir: string;

  /**
   * Timestamp of when the download was created.
   */
  created_at: string;

  /**
   * The total number of bytes that the download consists of if in progress.
   */
  total_bytes: number | null;

  /**
   * The speed of the download in bytes per second if in progress.
   */
  speed: number | null;

  /**
   * The number of bytes downloaded so far.
   */
  downloaded_bytes: number | null;

  /**
   * Timestamp of when the download terminated if so.
   */
  terminated_at: string | null;

  /**
   * Estimated time in seconds until the download completes.
   */
  eta: number | null;

  /**
   * An error message indicating the error that occurred if the download failed.
   */
  error_msg: string | null;
}

/**
 * Represents data emitted from the real-time API for the download_init event.
 */
export interface DownloadInitData {
  /**
   * A list of all downloads in the application and their states.
   */
  downloads: DownloadUpdate[];
}

/**
 * Represents the request body structure that must be sent with a restart download backend API request.
 */
export interface PostDownloadsRestartRequest {
  /**
   * A list of download IDs to restart.
   */
  download_ids: number[];
}

/**
 * Represents the various reponses that may be returned from a restart download backend API request.
 */
export type PostDownloadsRestartResponse =
  | {
      status: 400;
      body: {
        field: string;
        message: string;
      };
    }
  | {
      status: 200;
      body: {
        restart_count: number;
        message: string;
      };
    };

/**
 * Represents the request body structure that must be sent with a delete download backend API request.
 */
export interface DeleteDownloadsRequest {
  /**
   * A list of download IDs to delete.
   */
  download_ids: number[];
}

/**
 * Represents the various reponses that may be returned from a delete download backend API request.
 */
export type DeleteDownloadsReseponse =
  | {
      status: 400;
      body: {
        field: string;
        message: string;
      };
    }
  | {
      status: 200;
      body: {
        delete_count: number;
        message: string;
      };
    };
