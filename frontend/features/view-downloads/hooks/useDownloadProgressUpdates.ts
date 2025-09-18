import { useState, useEffect } from "react";
import downloadProgressSocket from "../services/downloadProgressSocket";
import type { DownloadProgressUpdate } from "../types";

export default function useDownloadProgressUpdates(
  connect: boolean,
  onComplete: (...args: any[]) => void
) {
  const [progress, setProgress] = useState<DownloadProgressUpdate | null>(null);
  const [recievingUpdates, setRecievingUpdtaes] = useState(false);

  useEffect(() => {
    setRecievingUpdtaes(!!progress);
  }, [progress]);

  const onProgress = (data: DownloadProgressUpdate) => {
    setProgress(data);
  };

  const onSubscribed = () => console.log("Subscribed to room 'download'.");

  useEffect(() => {
    if (!connect) return;

    const socket = downloadProgressSocket(onProgress, onSubscribed);

    socket.on("complete", () => {
      onComplete();
      setProgress(null);
    });

    return () => {
      socket.disconnect();
    };
  }, [connect]);

  return { progress, recievingUpdates };
}
