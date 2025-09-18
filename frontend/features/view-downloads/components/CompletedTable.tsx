import * as Ch from "@chakra-ui/react";
import DownloadsTableCard from "./shared/DownloadsTableCard";
import useGetDownloads from "../hooks/useGetDownloads";
import getDownloadTimeAgo from "../utils/getDownloadTimeAgo";
import DownloadsTable from "./shared/DownloadsTable";

export default function CompletedTable() {
  const { data } = useGetDownloads("completed");

  return (
    <DownloadsTableCard
      title="Completed"
      statusColorPalette="green"
      totalItems={data?.length}
    >
      <DownloadsTable
        data={data}
        emptyTitle="No Completed Downloads"
        emptyDesc="Completed downloads will appear here."
      >
        <Ch.Table.Header>
          <Ch.Table.Row>
            <Ch.Table.ColumnHeader>Track</Ch.Table.ColumnHeader>
            <Ch.Table.ColumnHeader>Codec/Collection</Ch.Table.ColumnHeader>
            <Ch.Table.ColumnHeader>Bitrate</Ch.Table.ColumnHeader>
            <Ch.Table.ColumnHeader>Completed At</Ch.Table.ColumnHeader>
          </Ch.Table.Row>
        </Ch.Table.Header>
        <Ch.Table.Body>
          <Ch.For each={data}>
            {(row) => (
              <Ch.Table.Row>
                <Ch.Table.Cell>{row.trackStr}</Ch.Table.Cell>
                <Ch.Table.Cell>{row.codec}</Ch.Table.Cell>
                <Ch.Table.Cell>
                  {row.codec === "mp3" && row.bitrate}
                </Ch.Table.Cell>
                <Ch.Table.Cell>
                  {getDownloadTimeAgo(row.completedAt as string)}
                </Ch.Table.Cell>
              </Ch.Table.Row>
            )}
          </Ch.For>
        </Ch.Table.Body>
      </DownloadsTable>
    </DownloadsTableCard>
  );
}
