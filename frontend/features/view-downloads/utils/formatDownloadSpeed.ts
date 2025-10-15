/**
 * Formats a download speed given in bytes per second to a human-readable string.
 *
 * @param bytesPerSec The download speed in bytes per second.
 * @returns The formatted string.
 */
export default function formatDownloadSpeed(
  bytesPerSec: number | null
): string {
  if (bytesPerSec === null) return "";

  const kb = bytesPerSec / 1024;
  const mb = bytesPerSec / (1024 * 1024);

  if (mb >= 1) {
    return `${mb.toFixed(1)} MB/s`;
  }

  return `${kb.toFixed(1)} kB/s`;
}
