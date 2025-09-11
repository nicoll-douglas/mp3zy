import { DownloadSettings, GeneralSettings } from "@/features/settings";
import PageHeading from "@/components/PageHeading";

export default function Settings() {
  return (
    <>
      <PageHeading>Settings</PageHeading>
      <DownloadSettings />
      <GeneralSettings />
    </>
  );
}
