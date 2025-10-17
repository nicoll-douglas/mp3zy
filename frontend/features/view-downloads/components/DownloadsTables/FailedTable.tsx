import * as Ch from "@chakra-ui/react";
import DownloadsTableCard from "./shared/DownloadsTableCard";
import { useDownloadsSocketContext } from "../../context/DownloadsSocketContext";
import getDownloadTimeAgo from "../../utils/getDownloadTimeAgo";
import useDownloadsSelection from "../../hooks/useDownloadsSelection";
import DownloadsTableCellCheckbox from "./shared/DownloadsTableCellCheckbox";
import DownloadsTableColumnHeaderCheckbox from "./shared/DownloadsTableColumnHeaderCheckbox";
import DownloadsSelectionActionBar from "./shared/DownloadsSelectionActionBar";
import { LuCircleMinus, LuRotateCw } from "react-icons/lu";

export default function FailedTable() {
  const { failed } = useDownloadsSocketContext();
  const downloadsSelection = useDownloadsSelection(failed);

  const failedWithEarliestFirst = failed.sort((a, b) => {
    if (!a.terminated_at || !b.terminated_at) return 0;

    return (
      new Date(a.terminated_at).getTime() - new Date(b.terminated_at).getTime()
    );
  });

  return (
    <>
      <DownloadsTableCard
        title="Failed Downloads"
        status="failed"
        totalItems={failed.length}
        emptyTitle="No Failed Downloads"
        emptyDesc="Failed downloads will appear here."
      >
        <Ch.Table.Root>
          <Ch.Table.Header>
            <Ch.Table.Row>
              <DownloadsTableColumnHeaderCheckbox
                downloadsSelection={downloadsSelection}
              />
              <Ch.Table.ColumnHeader>Main Artist</Ch.Table.ColumnHeader>
              <Ch.Table.ColumnHeader>Track Name</Ch.Table.ColumnHeader>
              <Ch.Table.ColumnHeader>Codec</Ch.Table.ColumnHeader>
              <Ch.Table.ColumnHeader>Bitrate</Ch.Table.ColumnHeader>
              <Ch.Table.ColumnHeader>Error</Ch.Table.ColumnHeader>
              <Ch.Table.ColumnHeader>Failed At</Ch.Table.ColumnHeader>
            </Ch.Table.Row>
          </Ch.Table.Header>
          <Ch.Table.Body>
            <Ch.For each={failedWithEarliestFirst}>
              {(download) => (
                <Ch.Table.Row
                  key={download.download_id}
                  data-selected={downloadsSelection.downloadRowSelected(
                    download
                  )}
                >
                  <DownloadsTableCellCheckbox
                    download={download}
                    downloadsSelection={downloadsSelection}
                  />
                  <Ch.Table.Cell>{download.artist_names[0]}</Ch.Table.Cell>
                  <Ch.TableCell>{download.track_name}</Ch.TableCell>
                  <Ch.Table.Cell>{download.codec}</Ch.Table.Cell>
                  <Ch.Table.Cell>
                    {download.codec === "mp3" && download.bitrate}
                  </Ch.Table.Cell>
                  <Ch.TableCell>{download.error_msg}</Ch.TableCell>
                  <Ch.TableCell>
                    {getDownloadTimeAgo(download.terminated_at)}
                  </Ch.TableCell>
                </Ch.Table.Row>
              )}
            </Ch.For>
          </Ch.Table.Body>
        </Ch.Table.Root>
      </DownloadsTableCard>
      <DownloadsSelectionActionBar
        tableStatus="failed"
        open={downloadsSelection.hasSelection}
        selectCount={downloadsSelection.selectionCount}
      >
        <Ch.Button colorPalette={"green"} variant={"surface"}>
          Restart
          <LuRotateCw />
        </Ch.Button>
        <Ch.Button colorPalette={"red"} variant={"surface"}>
          Remove
          <LuCircleMinus />
        </Ch.Button>
      </DownloadsSelectionActionBar>
    </>
  );
}
