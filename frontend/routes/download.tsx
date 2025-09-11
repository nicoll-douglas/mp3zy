import { DownloadSteps } from "@/features/download";
import PageHeading from "@/components/PageHeading";

export default function NewDownload() {
  return (
    <>
      <PageHeading>New Download</PageHeading>
      <DownloadSteps />
    </>
  );
}
