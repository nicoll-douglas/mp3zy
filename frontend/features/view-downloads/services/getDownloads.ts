import getBackendAuthHeaders from "@/services/getBackendAuthHeaders";
import type { DownloadRow, DownloadStatus } from "../types";

export default async function getDownloads(
  status: DownloadStatus
): Promise<DownloadRow[]> {
  const headers = getBackendAuthHeaders();
  const queryString = new URLSearchParams({ status }).toString();
  const res = await fetch(
    `${import.meta.env.VITE_BACKEND_URL}/downloads?${queryString}`,
    {
      headers,
    }
  );
  const body = await res.json();
  return body;
}
