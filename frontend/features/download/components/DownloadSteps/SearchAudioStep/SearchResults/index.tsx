import * as Ch from "@chakra-ui/react";
import SearchResultsEmptyState from "./SearchResultsEmptyState";
import { useAudioSearchContext } from "../../../../context/AudioSearchContext";
import DirectDownloadCard from "./DirectDownloadCard";
import SearchResultRadioCard from "./SearchResultRadioCard";

export default function SearchResults() {
  const {
    form,
    audioUrlSelected,
    onAudioSelectionChange,
    searchResults,
    searchStatus,
  } = useAudioSearchContext();

  return (
    <Ch.Show when={form.formState.isSubmitted}>
      <Ch.Card.Root size={"sm"}>
        <Ch.Card.Header>
          <Ch.Card.Title>Results</Ch.Card.Title>
          <Ch.Card.Description>{`${searchResults.length} total.`}</Ch.Card.Description>
        </Ch.Card.Header>
        <Ch.Card.Body>
          <Ch.Stack gap={"4"}>
            <Ch.RadioCard.Root
              value={audioUrlSelected}
              onValueChange={onAudioSelectionChange}
            >
              <Ch.RadioCard.Label>Select Source for Audio</Ch.RadioCard.Label>
              <Ch.Show when={searchStatus === "error"}>
                <SearchResultsEmptyState
                  title="Failed to search"
                  description={
                    <>
                      {/* TODO: add link to troubleshooting / app wiki */}
                      Something went wrong, try these{" "}
                      <Ch.Link>troubleshooting</Ch.Link> tips.
                    </>
                  }
                />
              </Ch.Show>
              <Ch.Show when={searchStatus === "success"}>
                <Ch.For
                  each={searchResults}
                  fallback={
                    <SearchResultsEmptyState
                      title="No Results"
                      description="Try adjusting your search."
                    />
                  }
                >
                  {(result, index) => (
                    <SearchResultRadioCard result={result} key={index} />
                  )}
                </Ch.For>
              </Ch.Show>
            </Ch.RadioCard.Root>
            <Ch.Show when={searchStatus === "success"}>
              <DirectDownloadCard />
            </Ch.Show>
          </Ch.Stack>
        </Ch.Card.Body>
      </Ch.Card.Root>
    </Ch.Show>
  );
}
