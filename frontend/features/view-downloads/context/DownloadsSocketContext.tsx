import { createContext, type ReactNode } from "react";
import useDownloadsSocket, {
  type UseDownloadsSocketReturn,
} from "../hooks/useDownloadsSocket";
import useSafeContext from "@/hooks/useContextSafe";

/**
 * The downloads socket context.
 */
export const DownloadsSocketContext =
  createContext<UseDownloadsSocketReturn | null>(null);

/**
 * Provider for the downloads socket context.
 *
 * Provides a shareable set of values returned from a useDownloadsSocket call.
 */
export function DownloadsSocketProvider({ children }: { children: ReactNode }) {
  const contextValue = useDownloadsSocket();

  return (
    <DownloadsSocketContext value={contextValue}>
      {children}
    </DownloadsSocketContext>
  );
}

/**
 * Hook to use the download sockets context.
 *
 * @returns The context value.
 */
export function useDownloadsSocketContext(): UseDownloadsSocketReturn {
  return useSafeContext<UseDownloadsSocketReturn>(DownloadsSocketContext);
}
