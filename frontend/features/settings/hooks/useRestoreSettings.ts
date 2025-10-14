import { useMutation, useQueryClient } from "@tanstack/react-query";

/**
 * Hook that provides a mutation to restore the application's default settings.
 *
 * @returns The mutation.
 */
export default function useRestoreSettings() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async () => window.electronAPI.restoreSettings(),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["settings"] }),
  });
}
