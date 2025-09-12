export interface YtDlpAudioSearchResult {
  channel: string;
  title: string;
  url: string;
  thumbnails: Array<{ height: number; width: number; url: string }>;
}

export type YtDlpSearchStatus = "error" | "success";

export interface YtDlpAudioSearchResponse {
  status: YtDlpSearchStatus;
  results: YtDlpAudioSearchResult[];
}
