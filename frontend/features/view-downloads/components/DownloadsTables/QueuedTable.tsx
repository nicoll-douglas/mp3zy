import * as Ch from "@chakra-ui/react";
import DownloadsTableCard from "./shared/DownloadsTableCard";
import { useDownloadsSocketContext } from "../../context/DownloadsSocketContext";
import getDownloadTimeAgo from "../../utils/getDownloadTimeAgo";

export default function QueuedTable() {
  const { queued } = useDownloadsSocketContext();

  const queuedWithEarliestFirst = queued.sort(
    (a, b) =>
      new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
  );

  return (
    <DownloadsTableCard
      title="Download Queue"
      statusColorPalette="yellow"
      totalItems={queued.length}
      emptyTitle="No Queued Downloads"
      emptyDesc="Queued downloads will appear here."
    >
      <Ch.Table.Root>
        <Ch.Table.Header>
          <Ch.Table.Row>
            <Ch.Table.ColumnHeader>Position</Ch.Table.ColumnHeader>
            <Ch.Table.ColumnHeader>Main Artist</Ch.Table.ColumnHeader>
            <Ch.Table.ColumnHeader>Track Name</Ch.Table.ColumnHeader>
            <Ch.Table.ColumnHeader>Codec</Ch.Table.ColumnHeader>
            <Ch.Table.ColumnHeader>Bitrate</Ch.Table.ColumnHeader>
            <Ch.Table.ColumnHeader>Ouput Directory</Ch.Table.ColumnHeader>
            <Ch.Table.ColumnHeader>Queued At</Ch.Table.ColumnHeader>
          </Ch.Table.Row>
        </Ch.Table.Header>
        <Ch.Table.Body>
          <Ch.For each={queuedWithEarliestFirst}>
            {(download, index) => (
              <Ch.Table.Row key={download.download_id}>
                <Ch.Table.Cell>{index + 1}</Ch.Table.Cell>
                <Ch.Table.Cell>{download.artist_names[0]}</Ch.Table.Cell>
                <Ch.TableCell>{download.track_name}</Ch.TableCell>
                <Ch.Table.Cell>{download.codec}</Ch.Table.Cell>
                <Ch.Table.Cell>
                  {download.codec === "mp3" && download.bitrate}
                </Ch.Table.Cell>
                <Ch.TableCell>{download.download_dir}</Ch.TableCell>
                <Ch.TableCell>
                  {getDownloadTimeAgo(download.created_at)}
                </Ch.TableCell>
              </Ch.Table.Row>
            )}
          </Ch.For>
        </Ch.Table.Body>
      </Ch.Table.Root>
    </DownloadsTableCard>
  );
}
