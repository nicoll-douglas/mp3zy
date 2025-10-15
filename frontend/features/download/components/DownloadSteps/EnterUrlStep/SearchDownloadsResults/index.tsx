import * as Ch from "@chakra-ui/react";
import SearchResultsEmptyState from "./SearchResultsEmptyState";
import { useSearchDownloadsFormContext } from "../../../../context/SearchDownloadsFormContext";
import SearchResultRadioCard from "./SearchResultRadioCard";
import { useDownloadFormContext } from "@/features/download/context/DownloadFormContext";

/**
 * Represents a card component that renders search results returned from a search downloads API request.
 */
export default function SearchDownloadsResults() {
  const { response } = useSearchDownloadsFormContext();
  const { form: downloadForm } = useDownloadFormContext();

  if (!response) return;

  const urlSelected = downloadForm.watch("url");

  return (
    <Ch.Card.Root size={"sm"}>
      <Ch.Card.Header>
        <Ch.Card.Title>Search Results</Ch.Card.Title>
        {response.status === 200 && (
          <Ch.Card.Description>{`${response.body.results.length} total.`}</Ch.Card.Description>
        )}
      </Ch.Card.Header>

      <Ch.Card.Body>
        {response.status === 200 ? (
          <Ch.Stack gap={"4"}>
            <Ch.RadioCard.Root
              value={urlSelected}
              onValueChange={(e) => {
                downloadForm.setValue("url", e.value ?? "");
              }}
            >
              <Ch.RadioCard.Label>Select Source for Audio</Ch.RadioCard.Label>
              <Ch.For
                each={response.body.results}
                fallback={
                  <SearchResultsEmptyState
                    title="No results"
                    description="Try adjusting your search or manually entering a URL."
                  />
                }
              >
                {(result, index) => (
                  <SearchResultRadioCard result={result} key={index} />
                )}
              </Ch.For>
            </Ch.RadioCard.Root>
          </Ch.Stack>
        ) : (
          <SearchResultsEmptyState
            title="Failed to Search"
            description={
              "Sorry, something went wrong. Try manually entering a URL."
            }
          />
        )}
      </Ch.Card.Body>
    </Ch.Card.Root>
  );
}
