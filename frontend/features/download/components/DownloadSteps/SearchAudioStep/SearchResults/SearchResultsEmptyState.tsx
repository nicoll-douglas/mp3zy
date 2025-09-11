import * as Ch from "@chakra-ui/react";
import { LuSearchX } from "react-icons/lu";

export default function SearchResultsEmptyState() {
  return (
    <Ch.EmptyState.Root>
      <Ch.EmptyState.Content>
        <Ch.EmptyState.Indicator>
          <LuSearchX />
        </Ch.EmptyState.Indicator>
        <Ch.VStack textAlign="center">
          <Ch.EmptyState.Title>No results</Ch.EmptyState.Title>
          <Ch.EmptyState.Description>
            Try adjusting your search.
          </Ch.EmptyState.Description>
        </Ch.VStack>
      </Ch.EmptyState.Content>
    </Ch.EmptyState.Root>
  );
}
