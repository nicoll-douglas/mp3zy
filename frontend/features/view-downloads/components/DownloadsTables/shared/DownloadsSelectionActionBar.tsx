import * as Ch from "@chakra-ui/react";
import { type DownloadStatus } from "../../../types";
import getDownloadStatusColorPalette from "../../../utils/getDownloadStatusColorPalette";
import type { ReactNode } from "react";

/**
 * Props for the DownloadsSelectionActionBar component.
 */
export interface DownloadsSelectionActionBarProps {
  /**
   * The status of the associated table of downloads.
   */
  tableStatus: DownloadStatus;

  /**
   * Whether the action bar should be open or not i.e there is a selection of downloads.
   */
  open: boolean;

  /**
   * The number of selected downloads.
   */
  selectCount: number;

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
  open,
  selectCount,
  children,
}: DownloadsSelectionActionBarProps) {
  return (
    <Ch.ActionBar.Root open={open}>
      <Ch.Portal>
        <Ch.ActionBar.Positioner>
          <Ch.ActionBar.Content>
            <Ch.ActionBar.SelectionTrigger>
              <Ch.Status.Root
                colorPalette={getDownloadStatusColorPalette(tableStatus)}
              >
                <Ch.Status.Indicator />
              </Ch.Status.Root>
              {selectCount} selected
            </Ch.ActionBar.SelectionTrigger>
            <Ch.ActionBar.Separator />
            {children}
          </Ch.ActionBar.Content>
        </Ch.ActionBar.Positioner>
      </Ch.Portal>
    </Ch.ActionBar.Root>
  );
}
