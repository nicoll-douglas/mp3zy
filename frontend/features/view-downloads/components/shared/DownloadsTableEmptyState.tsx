import * as Ch from "@chakra-ui/react";
import { LuListX } from "react-icons/lu";
import type React from "react";

export default function DownloadsTableEmptyState({
  title,
  description,
}: {
  title: string;
  description: React.ReactNode;
}) {
  return (
    <Ch.EmptyState.Root size={"sm"}>
      <Ch.EmptyState.Content>
        <Ch.EmptyState.Indicator>
          <LuListX />
        </Ch.EmptyState.Indicator>
        <Ch.VStack textAlign="center">
          <Ch.EmptyState.Title>{title}</Ch.EmptyState.Title>
          <Ch.EmptyState.Description>{description}</Ch.EmptyState.Description>
        </Ch.VStack>
      </Ch.EmptyState.Content>
    </Ch.EmptyState.Root>
  );
}
