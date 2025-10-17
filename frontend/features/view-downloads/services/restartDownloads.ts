import type {
  PostDownloadsRestartRequest,
  PostDownloadsRestartResponse,
} from "../types";

/**
 * Hits the backend API to restart downloads given IDs
 *
 * @param downloadIds The IDs of downloads to restart.
 * @returns The request response.
 */
export default async function restartDownloads(
  downloadIds: number[]
): Promise<PostDownloadsRestartResponse> {
  const endpoint = `${import.meta.env.VITE_BACKEND_URL}/downloads/restart`;

  const requestBody: PostDownloadsRestartRequest = {
    download_ids: downloadIds,
  };

  const res = await fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestBody),
  });

  const body = await res.json();

  return {
    status: res.status as PostDownloadsRestartResponse["status"],
    body,
  };
}
