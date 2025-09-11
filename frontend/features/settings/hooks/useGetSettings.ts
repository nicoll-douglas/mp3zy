import { useQuery } from "@tanstack/react-query";
import getSettings from "../services/getSettings";

export default function useGetSettings() {
  const query = useQuery({
    queryKey: ["settings", "savePath"],
    queryFn: getSettings,
  });

  return query;
}
