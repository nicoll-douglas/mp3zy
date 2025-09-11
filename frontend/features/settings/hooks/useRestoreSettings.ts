import { useMutation, useQueryClient } from "@tanstack/react-query";
import restoreSettings from "../services/restoreSettings";

export default function useRestoreSettings() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: restoreSettings,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["settings"] }),
  });

  return mutation;
}
