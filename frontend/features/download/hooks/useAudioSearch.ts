import { useState } from "react";
import { useForm } from "react-hook-form";
import type {
  YtDlpAudioSearchResponse,
  YtDlpAudioSearchResult,
  YtDlpSearchStatus,
} from "../types";
import type { SearchAudioFormValues } from "../forms/searchAudio";
import { type RadioCardValueChangeDetails } from "@chakra-ui/react";

export default function useAudioSearch(
  service: (track: string, artist: string) => Promise<YtDlpAudioSearchResponse>
) {
  const [audioUrlSelected, setAudioUrlSelected] = useState<string | null>(null);
  const form = useForm<SearchAudioFormValues>();
  const [searchResults, setSearchResults] = useState<YtDlpAudioSearchResult[]>(
    []
  );
  const [searchStatus, setSearchStatus] = useState<YtDlpSearchStatus | null>(
    null
  );

  const onFormSubmit = form.handleSubmit(async (data) => {
    const body = await service(data.track, data.artist);
    setSearchResults(body.results);
    setSearchStatus(body.status);
  });

  const onAudioSelectionChange = (e: RadioCardValueChangeDetails) =>
    setAudioUrlSelected(e.value);

  return {
    searchResults,
    searchStatus,
    audioUrlSelected,
    onAudioSelectionChange,
    form,
    onFormSubmit,
  };
}
