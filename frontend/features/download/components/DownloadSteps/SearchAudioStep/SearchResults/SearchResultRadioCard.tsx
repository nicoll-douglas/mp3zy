import type { YtDlpAudioSearchResult } from "../../../../types";
import * as Ch from "@chakra-ui/react";

export default function SearchResultRadioCard({
  result,
}: {
  result: YtDlpAudioSearchResult;
}) {
  return (
    <Ch.RadioCard.Item value={result.url} width="full">
      <Ch.RadioCard.ItemHiddenInput />
      <Ch.RadioCard.ItemControl>
        <Ch.HStack gap={"4"}>
          <Ch.RadioCard.ItemIndicator />
          <Ch.RadioCard.ItemContent>
            <Ch.Flex gap={"4"}>
              <Ch.Image
                src={result.thumbnails[0].url}
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
