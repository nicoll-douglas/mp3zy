import * as Ch from "@chakra-ui/react";
import { LuFolder } from "react-icons/lu";
import SettingsGroup from "./shared/SettingsGroup";
import useGetSettings from "../hooks/useGetSettings";
import useUpdateDownloadDir from "../hooks/useUpdateDownloadDir";

/**
 * Represents a card component that holds related settings to do with downloads.
 */
export default function DownloadSettings() {
  const getSettingsQuery = useGetSettings();
  const updateDownloadDirMutation = useUpdateDownloadDir();

  // if error in get query, then toast error "failed to load settings"
  // if error in update mutation, then toast error "failed to update settings"

  return (
    <SettingsGroup heading="Downloads">
      <Ch.Field.Root maxW={"lg"}>
        <Ch.Field.Label>Save Directory</Ch.Field.Label>
        <Ch.Group attached w="full">
          <Ch.Input
            value={getSettingsQuery.data?.default_download_dir}
            disabled
            cursor={"default"}
            title={getSettingsQuery.data?.default_download_dir}
            textOverflow={"ellipsis"}
          />
          <Ch.Button
            variant={"outline"}
            onClick={() => updateDownloadDirMutation.mutate()}
            disabled={updateDownloadDirMutation.isPending}
          >
            <LuFolder /> Change
          </Ch.Button>
        </Ch.Group>
        <Ch.Field.HelperText>
          The default directory on disk where downloaded tracks are saved.
        </Ch.Field.HelperText>
      </Ch.Field.Root>
    </SettingsGroup>
  );
}
