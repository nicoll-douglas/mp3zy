import { useQuery } from "@tanstack/react-query";

export default function useSettings() {
  const query = useQuery({
    queryKey: ["settings"],
    queryFn: async () => window.electronAPI.getSettings(),
  });

  return query;
}
