/**
 * Gets the progress of a download as a number out of 100 given the number of downloaded bytes and total bytes.
 *
 * @param downloadedBytes The number of currently downloaded bytes for the download.
 * @param totalBytes The total number of bytes of the download.
 * @returns The progress number.
 */
export default function getDownloadProgress(
  downloadedBytes: number,
  totalBytes: number
): number {
  if (totalBytes === 0) return 0;

  return Math.round((downloadedBytes / totalBytes) * 100);
}
