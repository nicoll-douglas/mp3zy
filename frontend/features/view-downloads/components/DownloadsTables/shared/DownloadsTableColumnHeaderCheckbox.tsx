import * as Ch from "@chakra-ui/react";
import { type UseDownloadsSelectionReturn } from "../../../hooks/useDownloadsSelection";

/**
 * Props for the DownloadsTableColumnHeaderCheckbox component.
 */
export interface DownloadsTableColumnHeaderCheckboxProps {
  /**
   * A value returned from a useDownloadsSelection hook call.
   */
  downloadsSelection: UseDownloadsSelectionReturn;
}

export default function DownloadsTableColumnHeaderCheckbox({
  downloadsSelection,
}: DownloadsTableColumnHeaderCheckboxProps) {
  return (
    <Ch.Table.ColumnHeader w="6">
      <Ch.Checkbox.Root
        size="sm"
        top="0.5"
        aria-label="Select all rows"
        checked={downloadsSelection.allChecked}
        onCheckedChange={downloadsSelection.onAllCheckedChange}
      >
        <Ch.Checkbox.HiddenInput />
        <Ch.Checkbox.Control />
      </Ch.Checkbox.Root>
    </Ch.Table.ColumnHeader>
  );
}
