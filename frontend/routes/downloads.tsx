import PageHeading from "@/components/PageHeading";
import { DownloadsTables } from "@/features/view-downloads";

export function meta() {
  return [{ title: `${import.meta.env.VITE_APP_NAME} | Downloads` }];
}

export default function Downloads() {
  return (
    <>
      <PageHeading>Downloads</PageHeading>
      <DownloadsTables />
    </>
  );
}
