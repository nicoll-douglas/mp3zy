import { DownloadSteps } from "@/features/download";
import PageHeading from "@/components/PageHeading";

export function meta() {
  return [{ title: `${import.meta.env.VITE_APP_NAME} | New Download` }];
}

export default function Download() {
  return (
    <>
      <PageHeading>New Download</PageHeading>
      <DownloadSteps />
    </>
  );
}
