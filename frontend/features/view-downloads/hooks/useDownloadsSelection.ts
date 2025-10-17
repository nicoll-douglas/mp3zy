import type { CheckboxCheckedChangeDetails } from "@chakra-ui/react";
import type { DownloadProgressUpdate } from "../types";
import { useState } from "react";

/**
 * Return type for the useDownloadsSelection hook.
 */
export interface UseDownloadsSelectionReturn {
  /**
   * Whether there is a current selection of downloads.
   */
  hasSelection: boolean;

  /**
   * The number of selected downloads.
   */
  selectionCount: number;

  /**
   * The state value for the "all checked" checkbox indicating whether all checkboxes are checked.
   */
  allChecked: "indeterminate" | boolean;

  /**
   * Handler to run when the all checked checkbox status changes.
   */
  onAllCheckedChange: (changes: CheckboxCheckedChangeDetails) => void;

  /**
   * Determines whether a download is currently checked (i.e in the selection).
   */
  downloadChecked: (download: DownloadProgressUpdate) => boolean;

  /**
   * Creates a handler to run when a download's checkbox value changes that updates the selection.
   */
  onDownloadCheckedChange: (
    download: DownloadProgressUpdate
  ) => (changes: CheckboxCheckedChangeDetails) => void;

  /**
   * Determines the value of the data-selected attribute for a row in the downloads table.
   */
  downloadRowSelected: (download: DownloadProgressUpdate) => "" | undefined;
}

/**
 * Hook to work with download selection and checkboxes in a downloads table.
 *
 * @param downloads The list of downloads that the table consists of.
 * @returns Event handlers and state values for selection state.
 */
export default function useDownloadsSelection(
  downloads: DownloadProgressUpdate[]
): UseDownloadsSelectionReturn {
  const [selection, setSelection] = useState<number[]>([]);

  const selectionCount = selection.length;
  const hasSelection = selectionCount > 0;
  const indeterminate = hasSelection && selectionCount < downloads.length;
  const allChecked = indeterminate ? "indeterminate" : selectionCount > 0;

  const onAllCheckedChange = (changes: CheckboxCheckedChangeDetails) => {
    setSelection(
      changes.checked ? downloads.map((download) => download.download_id) : []
    );
  };

  const downloadChecked = (download: DownloadProgressUpdate) =>
    selection.includes(download.download_id);

  const onDownloadCheckedChange = (download: DownloadProgressUpdate) => {
    return (changes: CheckboxCheckedChangeDetails) =>
      setSelection((prev) =>
        changes.checked
          ? [...prev, download.download_id]
          : selection.filter((id) => id !== download.download_id)
      );
  };

  const downloadRowSelected = (download: DownloadProgressUpdate) =>
    selection.includes(download.download_id) ? "" : undefined;

  return {
    hasSelection,
    allChecked,
    selectionCount,
    onAllCheckedChange,
    downloadChecked,
    onDownloadCheckedChange,
    downloadRowSelected,
  };
}
