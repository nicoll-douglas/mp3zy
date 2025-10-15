import type { DownloadFormValues } from "../forms/downloadForm";
import type { PostDownloadsResponse, PostDownloadsRequest } from "../types";

/**
 * Hits the backend API to start a download.
 *
 * @param data The validated form data from which to extract and send.
 * @returns The request response.
 */
export default async function startDownload(
  data: DownloadFormValues
): Promise<PostDownloadsResponse> {
  const endpoint = `${import.meta.env.VITE_BACKEND_URL}/downloads`;
  let releaseDate: PostDownloadsRequest["release_date"] = null;

  if (data.releaseYear !== "") {
    const year = Number.parseInt(data.releaseYear);

    if (data.releaseMonth === "") {
      releaseDate = {
        year,
        month: null,
        day: null,
      };
    } else {
      releaseDate = {
        year,
        month: Number.parseInt(data.releaseMonth),
        day: data.releaseDay === "" ? null : Number.parseInt(data.releaseDay),
      };
    }
  }

  const requestBody: PostDownloadsRequest = {
    artist_names: [
      data.artistNames[0].value,
      ...data.artistNames.slice(1).map((a) => a.value),
    ],
    track_name: data.trackName,
    album_name: data.albumName === "" ? null : data.albumName,
    codec: data.codec,
    bitrate: Number.parseInt(data.bitrate),
    track_number:
      data.trackNumber === "" ? null : Number.parseInt(data.trackNumber),
    disc_number:
      data.discNumber === "" ? null : Number.parseInt(data.discNumber),
    url: data.url,
    download_dir: data.downloadDir,
    album_cover_path: data.albumCoverPath === "" ? null : data.albumCoverPath,
    release_date: releaseDate,
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
    status: res.status as PostDownloadsResponse["status"],
    body,
  };
}
