import { io } from "socket.io-client";

export default function backendSocket() {
  const socket = io(import.meta.env.VITE_BACKEND_URL);
  return socket;
}
