import type { Bitrate, Codec } from "@/types";

export interface DownloadProgressUpdate {
  phase: "downloading" | "updating_metadata";
  progress: number;
  eta: string;
  speed: string;
  trackStr: string;
  codec: Codec;
  bitrate: Bitrate;
}

export type DownloadStatus = "failed" | "downloading" | "completed" | "queued";

export interface DownloadRow {
  codec: Codec;
  bitrate: Bitrate;
  error: string | null;
  createdAt: string;
  completedAt: string | null;
  updatedAt: string;
  trackStr: string;
}
