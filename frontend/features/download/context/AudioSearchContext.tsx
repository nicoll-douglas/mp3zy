import { createContext, useContext, type ReactNode } from "react";
import useAudioSearch from "../hooks/useAudioSearch";
import ytDlpAudioSearch from "../services/ytDlpAudioSearch";
import type { YtDlpAudioSearchResult } from "../types";
import type { SearchAudioFormValues } from "../forms/searchAudio";
import type { UseFormReturn } from "react-hook-form";
import type { RadioCardValueChangeDetails } from "@chakra-ui/react";

type AudioSearchContextValue = {
  searchResults: YtDlpAudioSearchResult[];
  audioUrlSelected: string | null;
  onAudioSelectionChange: (e: RadioCardValueChangeDetails) => void;
  form: UseFormReturn<SearchAudioFormValues, any, SearchAudioFormValues>;
  onFormSubmit: (e?: React.BaseSyntheticEvent) => Promise<void>;
} | null;

export const AudioSearchContext = createContext<AudioSearchContextValue>(null);

export function AudioSearchProvider({ children }: { children: ReactNode }) {
  const audioSearch = useAudioSearch(ytDlpAudioSearch);

  return (
    <AudioSearchContext value={audioSearch}>{children}</AudioSearchContext>
  );
}

export function useAudioSearchContext() {
  const value = useContext(AudioSearchContext);

  if (value === null) {
    throw new Error(
      "useContext must be used within context provider (AudioSearchContext"
    );
  }

  return value;
}
