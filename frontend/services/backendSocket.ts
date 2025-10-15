import { io } from "socket.io-client";

/**
 * Initializes a socket instance that will connect to the backend real-time API.
 *
 * @param namespace The namespace of the socket; defaults to the root.
 * @returns The socket instance.
 */
export default function backendSocket(namespace: string = "/") {
  return io(import.meta.env.VITE_BACKEND_URL + namespace, {
    autoConnect: false,
  });
}
