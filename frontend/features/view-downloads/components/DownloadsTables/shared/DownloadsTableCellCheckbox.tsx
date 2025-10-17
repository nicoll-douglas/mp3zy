import * as Ch from "@chakra-ui/react";
import { type UseDownloadsSelectionReturn } from "../../../hooks/useDownloadsSelection";
import type { DownloadProgressUpdate } from "@/features/view-downloads/types";

/**
 * Props for the DownloadsTableCellCheckbox component.
 */
export interface DownloadsTableCellCheckboxProps {
  /**
   * A value returned from a useDownloadsSelection hook call.
   */
  downloadsSelection: UseDownloadsSelectionReturn;

  /**
   * The download progress update pertaining to the current row of the table.
   */
  download: DownloadProgressUpdate;
}

export default function DownloadsTableCellCheckbox({
  downloadsSelection,
  download,
}: DownloadsTableCellCheckboxProps) {
  return (
    <Ch.Table.Cell>
      <Ch.Checkbox.Root
        size="sm"
        top="0.5"
        aria-label="Select row"
        checked={downloadsSelection.downloadChecked(download)}
        onCheckedChange={downloadsSelection.onDownloadCheckedChange(download)}
      >
        <Ch.Checkbox.HiddenInput />
        <Ch.Checkbox.Control />
      </Ch.Checkbox.Root>
    </Ch.Table.Cell>
  );
}
