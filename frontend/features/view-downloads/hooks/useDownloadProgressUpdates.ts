import { useState, useEffect } from "react";
import downloadProgressSocket from "../services/downloadProgressSocket";

export default function useDownloadProgressUpdates(taskId: string | null) {
  const [progress, setProgress] = useState(null);

  const onProgress = (data: any) => {
    if (data.taskId === taskId) {
      setProgress(data);
    }
  };

  const onSubscribed = () => console.log("Subscribed to task ID:", taskId);

  useEffect(() => {
    if (!taskId) return;

    const socket = downloadProgressSocket(taskId, onProgress, onSubscribed);

    return () => {
      socket.disconnect();
    };
  }, [taskId]);

  return progress;
}
