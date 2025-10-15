import { useState, useEffect } from "react";
import downloadsSocket from "../services/downloadsSocket";
import type { DownloadProgressUpdate, DownloadInitData } from "../types";

/**
 * Return type for the useDownloadsSocket hook.
 */
export interface UseDownloadsSocketReturn {
  completed: DownloadProgressUpdate[];
  failed: DownloadProgressUpdate[];
  queued: DownloadProgressUpdate[];
  downloading: DownloadProgressUpdate[];
}

/**
 * Hook that interfaces with downloads socket and returns the live data.
 *
 * @returns The live data which are lists of downloads based on status.
 */
export default function useDownloadsSocket(): UseDownloadsSocketReturn {
  const [allDownloads, setAllDownloads] = useState<{
    [key: number]: DownloadProgressUpdate;
  }>({});

  useEffect(() => {
    const socket = downloadsSocket();

    socket.on("download_init", (data: DownloadInitData) => {
      const downloadsMap: { [key: number]: DownloadProgressUpdate } = {};

      data.downloads.forEach((download) => {
        downloadsMap[download.download_id] = download;
      });

      setAllDownloads(downloadsMap);
    });

    socket.on("download_update", (data: DownloadProgressUpdate) => {
      setAllDownloads((v) => ({ ...v, [data.download_id]: data }));
    });

    socket.connect();

    return () => {
      socket.disconnect();
    };
  }, []);

  const downloadsList = Object.values(allDownloads);

  const completed = [];
  const failed = [];
  const queued = [];
  const downloading = [];

  for (let i = 0; i < downloadsList.length; i++) {
    switch (downloadsList[i].status) {
      case "completed":
        completed.push(downloadsList[i]);
        break;
      case "downloading":
        downloading.push(downloadsList[i]);
        break;
      case "failed":
        failed.push(downloadsList[i]);
        break;
      case "queued":
        queued.push(downloadsList[i]);
        break;
    }
  }

  return { completed, failed, queued, downloading };
}
