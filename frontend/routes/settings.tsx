import { DownloadSettings, GeneralSettings } from "@/features/settings";
import PageHeading from "@/components/PageHeading";

export function meta() {
  return [{ title: `${import.meta.env.VITE_APP_NAME} | Settings` }];
}

export default function Settings() {
  return (
    <>
      <PageHeading>Settings</PageHeading>
      <DownloadSettings />
      <GeneralSettings />
    </>
  );
}
