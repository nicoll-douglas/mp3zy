import { createContext, type ReactNode } from "react";
import useDownloadForm, {
  type UseDownloadFormReturn,
} from "../hooks/useDownloadForm";
import useSafeContext from "@/hooks/useContextSafe";

/**
 * The download form context.
 */
export const DownloadFormContext = createContext<UseDownloadFormReturn | null>(
  null
);

/**
 * Provider for the download form context.
 *
 * Provides a shareable set of values returned from a useDownloadForm call.
 */
export function DownloadFormProvider({ children }: { children: ReactNode }) {
  const contextValue = useDownloadForm();

  return (
    <DownloadFormContext value={contextValue}>{children}</DownloadFormContext>
  );
}

/**
 * Hook to use the download form context.
 *
 * @returns The context value.
 */
export function useDownloadFormContext(): UseDownloadFormReturn {
  return useSafeContext<UseDownloadFormReturn>(DownloadFormContext);
}
