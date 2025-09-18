import * as Ch from "@chakra-ui/react";
import DownloadsTableCard from "./shared/DownloadsTableCard";
import useGetDownloads from "../hooks/useGetDownloads";
import DownloadsTable from "./shared/DownloadsTable";
import getDownloadTimeAgo from "../utils/getDownloadTimeAgo";

export default function FailedTable() {
  const { data } = useGetDownloads("failed");

  return (
    <DownloadsTableCard
      title="Failed"
      statusColorPalette="red"
      totalItems={data?.length}
    >
      <DownloadsTable
        data={data}
        emptyTitle="No Failed Downloads"
        emptyDesc="Failed downloads will appear here."
      >
        <Ch.Table.Header>
          <Ch.Table.Row>
            <Ch.Table.ColumnHeader>Track</Ch.Table.ColumnHeader>
            <Ch.Table.ColumnHeader>Codec/Collection</Ch.Table.ColumnHeader>
            <Ch.Table.ColumnHeader>Bitrate</Ch.Table.ColumnHeader>
            <Ch.Table.ColumnHeader>Failed At</Ch.Table.ColumnHeader>
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
                  {getDownloadTimeAgo(row.updatedAt)}
                </Ch.Table.Cell>
              </Ch.Table.Row>
            )}
          </Ch.For>
        </Ch.Table.Body>
      </DownloadsTable>
    </DownloadsTableCard>
  );
}
