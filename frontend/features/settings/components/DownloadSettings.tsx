import * as Ch from "@chakra-ui/react";
import { LuFolder } from "react-icons/lu";
import SettingsGroup from "./shared/SettingsGroup";
import useGetSettings from "../hooks/useGetSettings";
import useUpdateDownloadDir from "../hooks/useUpdateDownloadDir";
import { Tooltip } from "@/components/chakra-ui/tooltip";

/**
 * Represents a card component that holds related settings to do with downloads.
 */
export default function DownloadSettings() {
  const getSettingsQuery = useGetSettings();
  const updateDownloadDirMutation = useUpdateDownloadDir();

  const defaultDownloadDir = getSettingsQuery.data?.default_download_dir;

  // if error in get query, then toast error "failed to load settings"
  // if error in update mutation, then toast error "failed to update settings"

  return (
    <SettingsGroup heading="Downloads">
      <Ch.Field.Root maxW={"lg"}>
        <Ch.Field.Label>Default Save Directory</Ch.Field.Label>
        <Ch.Group attached w="full">
          <Tooltip content={defaultDownloadDir} disabled={!defaultDownloadDir}>
            <Ch.Input
              value={defaultDownloadDir}
              disabled
              cursor={"default"}
              textOverflow={"ellipsis"}
              borderRight={"none"}
              borderRightRadius={0}
            />
          </Tooltip>
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
