import * as Ch from "@chakra-ui/react";
import DownloadsTableCard from "./shared/DownloadsTableCard";
import { useDownloadsSocketContext } from "../../context/DownloadsSocketContext";
import getDownloadTimeAgo from "../../utils/getDownloadTimeAgo";

export default function FailedTable() {
  const { failed } = useDownloadsSocketContext();

  const failedWithEarliestFirst = failed.sort((a, b) => {
    if (!a.terminated_at || !b.terminated_at) return 0;

    return (
      new Date(a.terminated_at).getTime() - new Date(b.terminated_at).getTime()
    );
  });

  return (
    <DownloadsTableCard
      title="Failed Downloads"
      statusColorPalette="red"
      totalItems={failed.length}
      emptyTitle="No Failed Downloads"
      emptyDesc="Failed downloads will appear here."
    >
      <Ch.Table.ScrollArea
        borderTopWidth={"1px"}
        borderRightWidth={"1px"}
        borderLeftWidth={"1px"}
        maxHeight={"500px"}
      >
        <Ch.Table.Root>
          <Ch.Table.Header>
            <Ch.Table.Row>
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
                <Ch.Table.Row key={download.download_id}>
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
      </Ch.Table.ScrollArea>
    </DownloadsTableCard>
  );
}
