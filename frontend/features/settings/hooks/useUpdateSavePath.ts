import { useQueryClient, useMutation } from "@tanstack/react-query";
import updateSavePath from "../services/updateSavePath";

export default function useUpdateSavePath() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: updateSavePath,
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: ["settings", "savePath"] }),
  });

  return mutation;
}
