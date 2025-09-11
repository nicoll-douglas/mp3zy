import backendSocket from "@/services/backendSocket";

export default function downloadProgressSocket(
  taskId: string,
  onProgress?: (...args: any[]) => void,
  onSubscribed?: (...args: any[]) => void
) {
  const socket = backendSocket();

  socket.on("connect", () => {
    console.log("Connected to backend via ws://");
    console.log("Socket ID:", socket.id);
    socket.emit("subscribe", { task_id: taskId });
  });

  if (onSubscribed) {
    socket.on("subscribed", onSubscribed);
  }

  if (onProgress) {
    socket.on("progress", onProgress);
  }

  return socket;
}
