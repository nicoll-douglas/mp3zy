export interface YtDlpAudioSearchResult {
  channel: string;
  title: string;
  url: string;
  thumbnails: Array<{ height: number; width: number; url: string }>;
}
