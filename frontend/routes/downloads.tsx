import PageHeading from "@/components/PageHeading";
import {
  DownloadingTable,
  QueueTable,
  FailedTable,
  CompletedTable,
} from "@/features/view-downloads";

export default function Downloads() {
  return (
    <>
      <PageHeading>Downloads</PageHeading>
      <DownloadingTable />
      <QueueTable />
      <FailedTable />
      <CompletedTable />
    </>
  );
}
