import * as Ch from "@chakra-ui/react";
import type { ReactNode } from "react";
import DownloadsTableEmptyState from "./DownloadsTableEmptyState";
import type { DownloadRow } from "../../types";

export default function DownloadsTable({
  children,
  emptyTitle,
  emptyDesc,
  data,
}: {
  children: ReactNode;
  emptyTitle: string;
  emptyDesc: ReactNode;
  data?: DownloadRow[];
}) {
  return (
    <>
      <Ch.Show when={data && data.length > 0}>
        <Ch.Table.Root>{children}</Ch.Table.Root>
      </Ch.Show>
      <Ch.Show when={data && data.length === 0}>
        <DownloadsTableEmptyState title={emptyTitle} description={emptyDesc} />
      </Ch.Show>
    </>
  );
}
