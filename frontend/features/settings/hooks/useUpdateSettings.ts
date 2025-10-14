import { useQueryClient, useMutation } from "@tanstack/react-query";
import type { UserSettings } from "types/shared";

/**
 * Hook that provides a mutation to update the application's settings.
 *
 * @returns The mutation.
 */
export default function useUpdateSettings() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (updatedSettings: Partial<UserSettings>) =>
      window.electronAPI.updateSettings(updatedSettings),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["settings"] }),
  });
}
