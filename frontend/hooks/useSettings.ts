import { useQuery, useQueryClient, useMutation } from "@tanstack/react-query";

export default function useSettings() {
  const getSettingsQuery = useQuery({
    queryKey: ["settings", "savePath"],
    queryFn: async () => window.electronAPI.getSettings(),
  });

  const queryClient = useQueryClient();

  const updateSavePathMutation = useMutation({
    mutationFn: async () => {
      const newSaveDir = await window.electronAPI.pickSaveDirectory();
      if (!newSaveDir) return;
      window.electronAPI.setSettings({ savePath: newSaveDir });
    },
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: ["settings", "savePath"] }),
  });

  const restoreSettingsMutation = useMutation({
    mutationFn: async () => window.electronAPI.restoreSettings(),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["settings"] }),
  });

  return { getSettingsQuery, updateSavePathMutation, restoreSettingsMutation };
}
