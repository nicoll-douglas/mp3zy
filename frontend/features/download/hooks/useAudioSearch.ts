import { useState } from "react";
import { useForm } from "react-hook-form";
import type { YtDlpAudioSearchResult } from "../types";
import type { SearchAudioFormValues } from "../forms/searchAudio";
import { type RadioCardValueChangeDetails } from "@chakra-ui/react";

export default function useAudioSearch(
  service: (track: string, artist: string) => Promise<YtDlpAudioSearchResult[]>
) {
  const [audioUrlSelected, setAudioUrlSelected] = useState<string | null>(null);
  const form = useForm<SearchAudioFormValues>();
  const [searchResults, setSearchResults] = useState<YtDlpAudioSearchResult[]>(
    []
  );

  const onFormSubmit = form.handleSubmit(async (data) => {
    const body = await service(data.track, data.artist);
    setSearchResults(body);
  });

  const onAudioSelectionChange = (e: RadioCardValueChangeDetails) =>
    setAudioUrlSelected(e.value);

  return {
    searchResults,
    audioUrlSelected,
    onAudioSelectionChange,
    form,
    onFormSubmit,
  };
}
