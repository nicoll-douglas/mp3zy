import type { Validate, RegisterOptions } from "react-hook-form";

export interface SearchAudioFormValues {
  artist: string;
  track: string;
}

export interface YtDlpAudioSearchResult {
  channel: string;
  title: string;
  url: string;
  thumbnails: Array<{ height: number; width: number; url: string }>;
}

export interface DownloadOptionsFormValues {
  artists: Array<{ value: string }>;
  track: string;
  album: string;
  codec: "mp3" | "flac";
  trackNumber: string;
  discNumber: string;
  bitrate: "128" | "192" | "320";
  year: string;
  month: string;
  day: string;
}

export type DownloadOptionsValidator = Validate<
  string | { value: string }[],
  DownloadOptionsFormValues
>;

export type DownloadOptionsControlRules = Omit<
  RegisterOptions<DownloadOptionsFormValues, keyof DownloadOptionsFormValues>,
  "setValueAs" | "disabled" | "valueAsNumber" | "valueAsDate"
>;
