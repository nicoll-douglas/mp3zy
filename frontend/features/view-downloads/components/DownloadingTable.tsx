import * as Ch from "@chakra-ui/react";
import DownloadsTableCard from "./shared/DownloadsTableCard";
import useDownloadProgressUpdates from "../hooks/useDownloadProgressUpdates";
import { useQueryClient } from "@tanstack/react-query";
import DownloadsTableEmptyState from "./shared/DownloadsTableEmptyState";
import { useEffect, useState } from "react";

export default function DownloadsTable() {
  const queryClient = useQueryClient();
  const onComplete = () => {
    queryClient.invalidateQueries({ queryKey: ["downloads", "completed"] });
  };
  const { progress, recievingUpdates } = useDownloadProgressUpdates(
    true,
    onComplete
  );

  useEffect(() => {
    if (recievingUpdates) {
      queryClient.invalidateQueries({ queryKey: ["downloads", "queued"] });
    }
  }, [recievingUpdates]);

  return (
    <DownloadsTableCard
      title="Currently Downloading"
      statusColorPalette="blue"
      totalItems={progress ? 1 : 0}
    >
      <Ch.Show when={!!progress}>
        <Ch.Table.Root>
          <Ch.Table.Header>
            <Ch.Table.Row>
              <Ch.Table.ColumnHeader>Track</Ch.Table.ColumnHeader>
              <Ch.Table.ColumnHeader>Codec/Collection</Ch.Table.ColumnHeader>
              <Ch.Table.ColumnHeader>Bitrate</Ch.Table.ColumnHeader>
              <Ch.Table.ColumnHeader>Progress</Ch.Table.ColumnHeader>
              <Ch.Table.ColumnHeader>ETA</Ch.Table.ColumnHeader>
              <Ch.Table.ColumnHeader>Speed</Ch.Table.ColumnHeader>
            </Ch.Table.Row>
          </Ch.Table.Header>
          <Ch.Table.Body>
            <Ch.Table.Row>
              <Ch.Table.Cell>{progress?.trackStr}</Ch.Table.Cell>
              <Ch.Table.Cell>{progress?.codec}</Ch.Table.Cell>
              <Ch.Table.Cell>{progress?.bitrate}</Ch.Table.Cell>
              <Ch.Table.Cell>
                <Ch.Progress.Root value={progress?.progress}>
                  <Ch.HStack gap={"2"}>
                    <Ch.Progress.Track flex={"1"}>
                      <Ch.Progress.Range />
                    </Ch.Progress.Track>
                    <Ch.Progress.ValueText />
                  </Ch.HStack>
                </Ch.Progress.Root>
              </Ch.Table.Cell>
              <Ch.Table.Cell>{progress?.eta}</Ch.Table.Cell>
              <Ch.Table.Cell>{progress?.speed}</Ch.Table.Cell>
            </Ch.Table.Row>
          </Ch.Table.Body>
        </Ch.Table.Root>
      </Ch.Show>
      <Ch.Show when={!progress}>
        <DownloadsTableEmptyState
          title="No Ongoing Downloads"
          description="Ongoing downloads will appear here."
        />
      </Ch.Show>
    </DownloadsTableCard>
  );
}
