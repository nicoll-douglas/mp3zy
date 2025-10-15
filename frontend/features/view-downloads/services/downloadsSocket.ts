import backendSocket from "@/services/backendSocket";

/**
 * Initializes socket instance that will connect to the /downloads namespace of the backend real-time API.
 *
 * @returns The socket instance.
 */
export default function downloadsSocket() {
  return backendSocket("/downloads");
}
