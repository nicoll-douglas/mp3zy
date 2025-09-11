import * as Ch from "@chakra-ui/react";
import { LuFolder } from "react-icons/lu";
import SettingsGroup from "./shared/SettingsGroup";
import useGetSettings from "../hooks/useGetSettings";
import useUpdateSavePath from "../hooks/useUpdateSavePath";

export default function DownloadSettings() {
  const getSettingsQuery = useGetSettings();
  const updateSavePathMutation = useUpdateSavePath();

  let savePath = "";
  if (getSettingsQuery.data) {
    savePath = getSettingsQuery.data.savePath;
  } else if (getSettingsQuery.isLoading) {
    savePath = "Loading...";
  } else if (getSettingsQuery.error) {
    savePath = getSettingsQuery.error.message;
  }

  return (
    <SettingsGroup heading="Downloads">
      <Ch.Field.Root maxW={"lg"}>
        <Ch.Field.Label>Save Directory</Ch.Field.Label>
        <Ch.Group attached w="full">
          <Ch.Input
            value={savePath}
            disabled
            cursor={"default"}
            title={savePath}
            textOverflow={"ellipsis"}
          />
          <Ch.Button
            variant={"outline"}
            onClick={() => updateSavePathMutation.mutate()}
            disabled={updateSavePathMutation.isPending}
          >
            <LuFolder /> Change
          </Ch.Button>
        </Ch.Group>
        <Ch.Field.HelperText>
          The directory on disk where music files downloaded and created are
          saved.
        </Ch.Field.HelperText>
      </Ch.Field.Root>
    </SettingsGroup>
  );
}
