import { useMutation } from "@tanstack/react-query";
import useUpdateSettings from "./useUpdateSettings";

/**
 * Hook that provides a mutation to update the `default_download_dir` field of the application settings.
 *
 * @returns The mutation.
 */
export default function useUpdateDownloadDir() {
  const updateSettingsMutation = useUpdateSettings();

  const mutation = useMutation({
    mutationFn: async () => {
      const newDownloadDir = await window.electronAPI.pickDirectory(
        "Select a New Default Download Directory"
      );

      if (!newDownloadDir) return;

      updateSettingsMutation.mutate({
        default_download_dir: newDownloadDir,
      });
    },
  });

  return mutation;
}
