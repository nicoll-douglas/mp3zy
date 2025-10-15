import { DownloadsSocketProvider } from "../../context/DownloadsSocketContext";
import CompletedTable from "./CompletedTable";
import DownloadingTable from "./DownloadingTable";
import QueuedTable from "./QueuedTable";
import FailedTable from "./FailedTable";

export default function DownloadsTables() {
  return (
    <DownloadsSocketProvider>
      <DownloadingTable />
      <QueuedTable />
      <FailedTable />
      <CompletedTable />
    </DownloadsSocketProvider>
  );
}
