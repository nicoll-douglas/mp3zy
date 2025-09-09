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
