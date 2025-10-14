import { useQuery } from "@tanstack/react-query";

/**
 * Hook to get settings with a query.
 *
 * @returns The settings query.
 */
export default function useGetSettings() {
  return useQuery({
    queryKey: ["settings"],
    queryFn: async () => window.electronAPI.getSettings(),
  });
}
