export default function getDownloadTimeAgo(dateStr: string | null): string {
  if (!dateStr) return "";

  const dt = new Date(dateStr.replace(" ", "T"));
  const now = new Date();

  const diff = (now.getTime() - dt.getTime()) / 1000;

  if (diff < 60) {
    return "Less than a minute ago";
  }

  if (diff < 60 * 60) {
    const mins = Math.floor(diff / 60);
    return `${mins} min${mins > 1 ? "s" : ""} ago`;
  }

  if (diff < 60 * 60 * 24) {
    const hours = Math.floor(diff / (60 * 60));
    return `${hours} hour${hours > 1 ? "s" : ""} ago`;
  }

  if (diff < 60 * 60 * 24 * 3) {
    const days = Math.floor(diff / (60 * 60 * 24));
    return `${days} day${days > 1 ? "s" : ""} ago`;
  }

  const day = dt.getDate().toString().padStart(2, "0");
  const month = (dt.getMonth() + 1).toString().padStart(2, "0"); // JS months are 0-based
  const year = dt.getFullYear();
  return `${day}-${month}-${year}`;
}
