import getBackendAuthHeaders from "@/services/getBackendAuthHeaders";
import type { YtDlpAudioSearchResponse } from "../types";

export default async function ytDlpAudioSearch(
  track: string,
  artist: string
): Promise<YtDlpAudioSearchResponse> {
  const headers = getBackendAuthHeaders();

  const queryString = new URLSearchParams({ track, artist }).toString();
  const res = await fetch(
    `${import.meta.env.VITE_BACKEND_URL}/audio-search/yt-dlp?${queryString}`,
    { headers }
  );
  const body = await res.json();
  return body;
}
