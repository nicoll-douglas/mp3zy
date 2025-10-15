/**
 * Formats an ETA time given in seconds to a HH:MM:SS or a MM:SS string.
 *
 * @param seconds The number of seconds.
 * @returns The formatted string.
 */
export default function formatEta(seconds: number | null | undefined): string {
  if (seconds == null) {
    return "";
  }

  const totalSeconds = Math.round(seconds);
  const hours = Math.floor(totalSeconds / 3600);
  const remainder = totalSeconds % 3600;
  const minutes = Math.floor(remainder / 60);
  const secs = remainder % 60;

  if (hours > 0) {
    return `${hours.toString().padStart(2, "0")}:${minutes
      .toString()
      .padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  }

  return `${minutes.toString().padStart(2, "0")}:${secs
    .toString()
    .padStart(2, "0")}`;
}
