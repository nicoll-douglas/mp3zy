import * as Ch from "@chakra-ui/react";
import type { ReactNode } from "react";
import DownloadsTableEmptyState from "./DownloadsTableEmptyState";
import type { DownloadStatus } from "../../../types";
import getDownloadStatusColorPalette from "../../../utils/getDownloadStatusColorPalette";

/**
 * Props for the DownloadsTableCard component.
 */
export interface DownloadsTableCardProps {
  /**
   * The title of the card.
   */
  title: string;

  /**
   * Children, i.e the downloads table.
   */
  children: ReactNode;

  /**
   * The total number of downloads.
   */
  totalItems: number;

  /**
   * The status of the download table.
   */
  status: DownloadStatus;

  /**
   * The title to show when there are no downloads.
   */
  emptyTitle: string;

  /**
   * The description/message to show when there are no downloads.
   */
  emptyDesc: string;
}

/**
 * Represents a card that will contain a table of downloads or an empty state if there are none.
 */
export default function DownloadsTableCard({
  title,
  children,
  totalItems,
  emptyTitle,
  emptyDesc,
  status,
}: DownloadsTableCardProps) {
  return (
    <Ch.Card.Root size={"sm"}>
      <Ch.Card.Header>
        <Ch.Status.Root
          size={"lg"}
          colorPalette={getDownloadStatusColorPalette(status)}
        >
          <Ch.Status.Indicator />
          <Ch.Card.Title>{title}</Ch.Card.Title>
        </Ch.Status.Root>
        <Ch.Card.Description>{totalItems} total.</Ch.Card.Description>
      </Ch.Card.Header>
      <Ch.Card.Body>
        <Ch.Show when={totalItems > 0}>
          <Ch.Table.ScrollArea
            borderTopWidth={"1px"}
            borderRightWidth={"1px"}
            borderLeftWidth={"1px"}
            maxHeight={"500px"}
          >
            {children}
          </Ch.Table.ScrollArea>
        </Ch.Show>
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
