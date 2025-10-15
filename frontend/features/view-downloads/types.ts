import type { TrackCodec, TrackBitrate, TrackArtistNames } from "@/types";

/**
 * Represents the possible statuses that a download can be in.
 */
export type DownloadStatus = "failed" | "downloading" | "completed" | "queued";

/**
 * A download update pertaining to data that may be received from the backend real-time API about a download.
 */
export interface DownloadProgressUpdate {
  download_id: number;
  status: DownloadStatus;
  artist_names: TrackArtistNames;
  track_name: string;
  codec: TrackCodec;
  bitrate: TrackBitrate;
  url: string;
  download_dir: string;
  created_at: string;
  total_bytes: number | null;
  speed: number | null;
  downloaded_bytes: number | null;
  terminated_at: string | null;
  eta: number | null;
  error_msg: string | null;
}

/**
 * Represents data emitted from the real-time API for the download_init event.
 */
export interface DownloadInitData {
  downloads: DownloadProgressUpdate[];
}
