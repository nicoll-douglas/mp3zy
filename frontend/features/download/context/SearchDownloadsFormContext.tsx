import { createContext, type ReactNode } from "react";
import useSearchDownloadsForm, {
  type UseSearchDownloadsFormReturn,
} from "../hooks/useSearchDownloadsForm";
import useSafeContext from "@/hooks/useContextSafe";

/**
 * The search downloads form context.
 */
export const SearchDownloadsFormContext =
  createContext<UseSearchDownloadsFormReturn | null>(null);

/**
 * Provider for the search downloads form context.
 *
 * Provides a shareable set of values returned from a useSearchDownloadsForm call.
 */
export function SearchDownloadsFormProvider({
  children,
}: {
  children: ReactNode;
}) {
  const contextValue = useSearchDownloadsForm();

  return (
    <SearchDownloadsFormContext value={contextValue}>
      {children}
    </SearchDownloadsFormContext>
  );
}

/**
 * Hook to use the search downloads form context.
 *
 * @returns The context value.
 */
export function useSearchDownloadsFormContext() {
  return useSafeContext<UseSearchDownloadsFormReturn>(
    SearchDownloadsFormContext
  );
}
