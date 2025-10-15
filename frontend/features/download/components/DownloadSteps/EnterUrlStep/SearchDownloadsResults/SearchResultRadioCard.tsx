import type { DownloadSearchResult } from "../../../../types";
import * as Ch from "@chakra-ui/react";

/**
 * Props for the SearchResultRadioCard component.
 */
export interface SearchResultRadioCardProps {
  /**
   * The download search result holding the information to render.
   */
  result: DownloadSearchResult;
}

/**
 * Represents a radio card component that displays a download search result with thumbnail, title, url, etc.
 */
export default function SearchResultRadioCard({
  result,
}: SearchResultRadioCardProps) {
  return (
    <Ch.RadioCard.Item value={result ? result.url : ""} width="full">
      <Ch.RadioCard.ItemHiddenInput />
      <Ch.RadioCard.ItemControl>
        <Ch.HStack gap={"4"}>
          <Ch.RadioCard.ItemIndicator />
          <Ch.RadioCard.ItemContent>
            <Ch.Flex gap={"4"}>
              <Ch.Image
                src={result.thumbnail || undefined}
                width={180}
                borderRadius={"sm"}
              />
              <Ch.Box>
                <Ch.RadioCard.ItemText wordBreak={"break-word"}>
                  {result.title}
                </Ch.RadioCard.ItemText>
                <Ch.Text>{result.channel}</Ch.Text>
                <Ch.Link href={result.url} wordBreak={"break-all"}>
                  {result.url}
                </Ch.Link>
              </Ch.Box>
            </Ch.Flex>
          </Ch.RadioCard.ItemContent>
        </Ch.HStack>
      </Ch.RadioCard.ItemControl>
    </Ch.RadioCard.Item>
  );
}
