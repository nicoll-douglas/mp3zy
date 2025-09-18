import backendSocket from "@/services/backendSocket";

export default function downloadProgressSocket(
  onProgress?: (...args: any[]) => void,
  onSubscribed?: (...args: any[]) => void
) {
  const socket = backendSocket();

  let socketId: string | undefined;

  socket.on("connect", () => {
    socketId = socket.id;
    console.log("Socket connected, ID:", socketId);
    socket.emit("subscribe", { room_id: "download" });
  });

  socket.on("disconnect", () => {
    console.log("Socket disconnected, ID:", socketId);
  });

  if (onSubscribed) {
    socket.on("subscribed", onSubscribed);
  }

  if (onProgress) {
    socket.on("progress", onProgress);
  }

  return socket;
}
