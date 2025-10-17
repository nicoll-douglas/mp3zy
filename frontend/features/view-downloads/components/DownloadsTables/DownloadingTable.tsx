import * as Ch from "@chakra-ui/react";
import DownloadsTableCard from "./shared/DownloadsTableCard";
import { useDownloadsSocketContext } from "../../context/DownloadsSocketContext";
import getDownloadProgress from "../../utils/getDownloadProgress";
import formatEta from "../../utils/formatEta";
import formatDownloadSpeed from "../../utils/formatDownloadSpeed";

export default function DownloadsTable() {
  const { downloading } = useDownloadsSocketContext();

  return (
    <DownloadsTableCard
      title="Currently Downloading"
      status="downloading"
      totalItems={downloading.length}
      emptyTitle="No Ongoing Downloads"
      emptyDesc="Ongoing downloads will appear here."
    >
      <Ch.Table.Root>
        <Ch.Table.Header>
          <Ch.Table.Row>
            <Ch.Table.ColumnHeader>Track Name</Ch.Table.ColumnHeader>
            <Ch.Table.ColumnHeader>Main Artist</Ch.Table.ColumnHeader>
            <Ch.Table.ColumnHeader>Codec</Ch.Table.ColumnHeader>
            <Ch.Table.ColumnHeader>Bitrate</Ch.Table.ColumnHeader>
            <Ch.Table.ColumnHeader>Output Directory</Ch.Table.ColumnHeader>
            <Ch.Table.ColumnHeader>Progress</Ch.Table.ColumnHeader>
            <Ch.Table.ColumnHeader>ETA</Ch.Table.ColumnHeader>
            <Ch.Table.ColumnHeader>Speed</Ch.Table.ColumnHeader>
          </Ch.Table.Row>
        </Ch.Table.Header>
        <Ch.Table.Body>
          <Ch.For each={downloading}>
            {(download) => (
              <Ch.Table.Row key={download.download_id}>
                <Ch.Table.Cell>{download.track_name}</Ch.Table.Cell>
                <Ch.Table.Cell>{download.artist_names[0]}</Ch.Table.Cell>
                <Ch.Table.Cell>{download.codec}</Ch.Table.Cell>
                <Ch.Table.Cell>
                  {download.codec === "mp3" && download.bitrate}
                </Ch.Table.Cell>
                <Ch.TableCell>{download.download_dir}</Ch.TableCell>
                <Ch.Table.Cell>
                  {download.downloaded_bytes !== null &&
                    download.total_bytes !== null && (
                      <Ch.Progress.Root
                        value={getDownloadProgress(
                          download.downloaded_bytes,
                          download.total_bytes
                        )}
                      >
                        <Ch.HStack gap={"2"}>
                          <Ch.Progress.Track flex={"1"}>
                            <Ch.Progress.Range />
                          </Ch.Progress.Track>
                          <Ch.Progress.ValueText />
                        </Ch.HStack>
                      </Ch.Progress.Root>
                    )}
                </Ch.Table.Cell>
                <Ch.Table.Cell>{formatEta(download.eta)}</Ch.Table.Cell>
                <Ch.Table.Cell>
                  {formatDownloadSpeed(download.speed)}
                </Ch.Table.Cell>
              </Ch.Table.Row>
            )}
          </Ch.For>
        </Ch.Table.Body>
      </Ch.Table.Root>
    </DownloadsTableCard>
  );
}
