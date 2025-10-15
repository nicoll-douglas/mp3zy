import * as Ch from "@chakra-ui/react";
import { LuSearchX } from "react-icons/lu";
import type { ReactNode } from "react";

/**
 * Props for the SearchResultsEmptyState component.
 */
interface SearchResultsEmptyStateProps {
  /**
   * The title of the empty state.
   */
  title: ReactNode;

  /**
   * The description of the empty state.
   */
  description: ReactNode;
}

/**
 * Represents an empty state to display to the user for when there are no search results.
 */
export default function SearchResultsEmptyState({
  title,
  description,
}: SearchResultsEmptyStateProps) {
  return (
    <Ch.EmptyState.Root>
      <Ch.EmptyState.Content>
        <Ch.EmptyState.Indicator>
          <LuSearchX />
        </Ch.EmptyState.Indicator>
        <Ch.VStack textAlign="center">
          <Ch.EmptyState.Title>{title}</Ch.EmptyState.Title>
          <Ch.EmptyState.Description>{description}</Ch.EmptyState.Description>
        </Ch.VStack>
      </Ch.EmptyState.Content>
    </Ch.EmptyState.Root>
  );
}
