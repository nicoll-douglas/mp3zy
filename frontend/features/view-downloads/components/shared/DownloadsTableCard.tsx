import * as Ch from "@chakra-ui/react";
import type { ReactNode } from "react";

export default function DownloadsTableCard({
  title,
  statusColorPalette,
  children,
  totalItems,
}: {
  children: ReactNode;
  statusColorPalette: "blue" | "green" | "red" | "yellow" | "orange";
  title: string;
  totalItems?: number;
}) {
  return (
    <Ch.Card.Root size={"sm"}>
      <Ch.Card.Header>
        <Ch.Status.Root size={"lg"} colorPalette={statusColorPalette}>
          <Ch.Status.Indicator />
          <Ch.Card.Title>{title}</Ch.Card.Title>
        </Ch.Status.Root>
        <Ch.Show when={!!totalItems}>
          <Ch.Card.Description>{totalItems} total.</Ch.Card.Description>
        </Ch.Show>
      </Ch.Card.Header>
      <Ch.Card.Body>{children}</Ch.Card.Body>
    </Ch.Card.Root>
  );
}
