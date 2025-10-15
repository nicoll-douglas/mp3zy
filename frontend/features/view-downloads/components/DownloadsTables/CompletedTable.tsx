import * as Ch from "@chakra-ui/react";
import DownloadsTableCard from "./shared/DownloadsTableCard";
import { useDownloadsSocketContext } from "../../context/DownloadsSocketContext";
import getDownloadTimeAgo from "../../utils/getDownloadTimeAgo";

export default function CompletedTable() {
  const { completed } = useDownloadsSocketContext();

  return (
    <DownloadsTableCard
      title="Completed"
      statusColorPalette="green"
      totalItems={completed.length}
      emptyTitle="No Completed Downloads"
      emptyDesc="Completed downloads will appear here."
    >
      <Ch.Table.Root>
        <Ch.Table.Header>
          <Ch.Table.Row>
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
              <Ch.Table.Row key={download.download_id}>
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
  );
}
