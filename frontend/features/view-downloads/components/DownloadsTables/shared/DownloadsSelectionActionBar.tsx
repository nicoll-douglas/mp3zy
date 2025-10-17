import * as Ch from "@chakra-ui/react";
import { type DownloadStatus } from "../../../types";
import getDownloadStatusColorPalette from "../../../utils/getDownloadStatusColorPalette";
import type { ReactNode } from "react";
import type { UseDownloadsSelectionReturn } from "../../../hooks/useDownloadsSelection";

/**
 * Props for the DownloadsSelectionActionBar component.
 */
export interface DownloadsSelectionActionBarProps {
  /**
   * The status of the associated table of downloads.
   */
  tableStatus: DownloadStatus;

  /**
   * A value returned from a useDownloadsSelection hook call.
   */
  downloadsSelection: UseDownloadsSelectionReturn;

  /**
   * Children i.e the actions.
   */
  children: ReactNode;
}

/**
 * An action bar that will contain actions for managing a selection fo downloads.
 */
export default function DownloadsSelectionActionBar({
  tableStatus,
  downloadsSelection,
  children,
}: DownloadsSelectionActionBarProps) {
  return (
    <Ch.ActionBar.Root open={downloadsSelection.hasSelection}>
      <Ch.Portal>
        <Ch.ActionBar.Positioner>
          <Ch.ActionBar.Content>
            <Ch.ActionBar.SelectionTrigger>
              <Ch.Status.Root
                colorPalette={getDownloadStatusColorPalette(tableStatus)}
              >
                <Ch.Status.Indicator />
              </Ch.Status.Root>
              {downloadsSelection.selectionCount} selected
            </Ch.ActionBar.SelectionTrigger>
            <Ch.ActionBar.Separator />
            {children}
          </Ch.ActionBar.Content>
        </Ch.ActionBar.Positioner>
      </Ch.Portal>
    </Ch.ActionBar.Root>
  );
}
