import type { DownloadStatus } from "../types";

/**
 * Gets the color palette associated with a download's status.
 *
 * @param status The download status.
 * @returns The color palette.
 */
export default function getDownloadStatusColorPalette(status: DownloadStatus) {
  switch (status) {
    case "completed":
      return "green";
    case "downloading":
      return "blue";
    case "failed":
      return "red";
    case "queued":
      return "yellow";
  }
}
