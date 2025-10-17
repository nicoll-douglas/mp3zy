import type {
  DeleteDownloadsRequest,
  DeleteDownloadsReseponse,
} from "../types";

/**
 * Hits the backend API to delete downloads given IDs
 *
 * @param downloadIds The IDs of downloads to delete.
 * @returns The request response.
 */
export default async function deleteDownloads(
  downloadIds: number[]
): Promise<DeleteDownloadsReseponse> {
  const endpoint = `${import.meta.env.VITE_BACKEND_URL}/downloads`;

  const requestBody: DeleteDownloadsRequest = {
    download_ids: downloadIds,
  };

  const res = await fetch(endpoint, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestBody),
  });

  const body = await res.json();

  return {
    status: res.status as DeleteDownloadsReseponse["status"],
    body,
  };
}
