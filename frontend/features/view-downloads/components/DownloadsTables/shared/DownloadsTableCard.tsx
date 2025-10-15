import * as Ch from "@chakra-ui/react";
import type { ReactNode } from "react";
import DownloadsTableEmptyState from "./DownloadsTableEmptyState";

export default function DownloadsTableCard({
  title,
  statusColorPalette,
  children,
  totalItems,
  emptyTitle,
  emptyDesc,
}: {
  children: ReactNode;
  statusColorPalette: "blue" | "green" | "red" | "yellow" | "orange";
  title: string;
  totalItems: number;
  emptyTitle: string;
  emptyDesc: string;
}) {
  return (
    <Ch.Card.Root size={"sm"}>
      <Ch.Card.Header>
        <Ch.Status.Root size={"lg"} colorPalette={statusColorPalette}>
          <Ch.Status.Indicator />
          <Ch.Card.Title>{title}</Ch.Card.Title>
        </Ch.Status.Root>
        <Ch.Card.Description>{totalItems} total.</Ch.Card.Description>
      </Ch.Card.Header>
      <Ch.Card.Body>
        <Ch.Show when={totalItems > 0}>{children}</Ch.Show>
        <Ch.Show when={totalItems === 0}>
          <DownloadsTableEmptyState
            title={emptyTitle}
            description={emptyDesc}
          />
        </Ch.Show>
      </Ch.Card.Body>
    </Ch.Card.Root>
  );
}
