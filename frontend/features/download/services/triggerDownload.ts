import type { DownloadOptionsFormValues } from "../forms/downloadOptions";
import getBackendAuthHeaders from "@/services/getBackendAuthHeaders";

export default async function triggerDownload(
  audioUrl: string | null,
  data: DownloadOptionsFormValues
): Promise<{ taskId: string }> {
  const headers = getBackendAuthHeaders();
  const requestUrl = `${import.meta.env.VITE_BACKEND_URL}/download`;

  const res = await fetch(requestUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...headers,
    },
    body: JSON.stringify({
      ...data,
      downloadUrl: audioUrl,
      artists: data.artists.map((a) => a.value),
    }),
  });
  const body = await res.json();
  return body;
}
