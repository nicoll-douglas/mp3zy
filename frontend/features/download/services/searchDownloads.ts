import type {
  GetDownloadsSearchRequest,
  GetDownloadsSearchResponse,
} from "../types";

/**
 * Hits the backend API to query for download search results.
 *
 * @param query The query parameters.
 * @returns The request response.
 */
export default async function searchDownloads(
  query: GetDownloadsSearchRequest
): Promise<GetDownloadsSearchResponse> {
  const queryString = new URLSearchParams({ ...query }).toString();
  const res = await fetch(
    `${import.meta.env.VITE_BACKEND_URL}/downloads/search?${queryString}`
  );

  const body = await res.json();

  return {
    status: res.status as GetDownloadsSearchResponse["status"],
    body,
  };
}
