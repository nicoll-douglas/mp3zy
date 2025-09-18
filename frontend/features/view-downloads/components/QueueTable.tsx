import * as Ch from "@chakra-ui/react";
import DownloadsTableCard from "./shared/DownloadsTableCard";
import useGetDownloads from "../hooks/useGetDownloads";
import DownloadsTable from "./shared/DownloadsTable";

export default function QueueTable() {
  const { data } = useGetDownloads("queued");

  return (
    <DownloadsTableCard
      title="Queued"
      totalItems={data?.length}
      statusColorPalette="yellow"
    >
      <DownloadsTable
        data={data}
        emptyTitle="No Queued Downloads"
        emptyDesc="Queued downloads will appear here."
      >
        <Ch.Table.Header>
          <Ch.Table.Row>
            <Ch.Table.ColumnHeader>Number</Ch.Table.ColumnHeader>
            <Ch.Table.ColumnHeader>Track</Ch.Table.ColumnHeader>
            <Ch.Table.ColumnHeader>Codec/Collection</Ch.Table.ColumnHeader>
            <Ch.Table.ColumnHeader>Bitrate</Ch.Table.ColumnHeader>
          </Ch.Table.Row>
        </Ch.Table.Header>
        <Ch.Table.Body>
          <Ch.For each={data}>
            {(row, index) => (
              <Ch.Table.Row>
                <Ch.Table.Cell>{index + 1}</Ch.Table.Cell>
                <Ch.Table.Cell>{row.trackStr}</Ch.Table.Cell>
                <Ch.Table.Cell>{row.codec}</Ch.Table.Cell>
                <Ch.Table.Cell>
                  {row.codec === "mp3" && row.bitrate}
                </Ch.Table.Cell>
              </Ch.Table.Row>
            )}
          </Ch.For>
        </Ch.Table.Body>
      </DownloadsTable>
    </DownloadsTableCard>
  );
}
