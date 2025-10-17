import * as Ch from "@chakra-ui/react";
import DownloadsTableCard from "./shared/DownloadsTableCard";
import { useDownloadsSocketContext } from "../../context/DownloadsSocketContext";
import getDownloadTimeAgo from "../../utils/getDownloadTimeAgo";
import useDownloadsSelection from "../../hooks/useDownloadsSelection";
import DownloadsTableColumnHeaderCheckbox from "./shared/DownloadsTableColumnHeaderCheckbox";
import DownloadsTableCellCheckbox from "./shared/DownloadsTableCellCheckbox";
import DownloadsSelectionActionBar from "./shared/DownloadsSelectionActionBar";
import deleteDownloads from "../../services/deleteDownloads";
import { LuCircleMinus } from "react-icons/lu";

export default function CompletedTable() {
  const { completed } = useDownloadsSocketContext();
  const downloadsSelection = useDownloadsSelection(completed);

  const handleDelete = async () => {
    const res = await deleteDownloads(downloadsSelection.selection);

    if (res.status === 200) {
      downloadsSelection.resetSelection();
    }
  };

  return (
    <>
      <DownloadsTableCard
        title="Completed"
        status="completed"
        totalItems={completed.length}
        emptyTitle="No Completed Downloads"
        emptyDesc="Completed downloads will appear here."
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
              <Ch.Table.ColumnHeader>Output Directory</Ch.Table.ColumnHeader>
              <Ch.Table.ColumnHeader>Completed At</Ch.Table.ColumnHeader>
            </Ch.Table.Row>
          </Ch.Table.Header>
          <Ch.Table.Body>
            <Ch.For each={completed}>
              {(download) => (
                <Ch.Table.Row
                  key={download.download_id}
                  data-selected={downloadsSelection.downloadRowSelected(
                    download
                  )}
                >
                  <DownloadsTableCellCheckbox
                    downloadsSelection={downloadsSelection}
                    download={download}
                  />
                  <Ch.Table.Cell>{download.artist_names[0]}</Ch.Table.Cell>
                  <Ch.Table.Cell>{download.track_name}</Ch.Table.Cell>
                  <Ch.Table.Cell>{download.codec}</Ch.Table.Cell>
                  <Ch.Table.Cell>
                    {download.codec === "mp3" && download.bitrate}
                  </Ch.Table.Cell>
                  <Ch.TableCell>{download.download_dir}</Ch.TableCell>
                  <Ch.Table.Cell>
                    {getDownloadTimeAgo(download.terminated_at)}
                  </Ch.Table.Cell>
                </Ch.Table.Row>
              )}
            </Ch.For>
          </Ch.Table.Body>
        </Ch.Table.Root>
      </DownloadsTableCard>
      <DownloadsSelectionActionBar
        tableStatus="completed"
        downloadsSelection={downloadsSelection}
      >
        <Ch.Button
          colorPalette={"red"}
          variant={"surface"}
          onClick={handleDelete}
        >
          Remove
          <LuCircleMinus />
        </Ch.Button>
      </DownloadsSelectionActionBar>
    </>
  );
}
