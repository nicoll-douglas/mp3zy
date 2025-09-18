import { useQuery } from "@tanstack/react-query";
import getDownloads from "../services/getDownloads";
import type { DownloadStatus } from "../types";

export default function useGetDownloads(status: DownloadStatus) {
  const query = useQuery({
    queryKey: ["downloads", status],
    queryFn: async () => getDownloads(status),
  });

  return query;
}
