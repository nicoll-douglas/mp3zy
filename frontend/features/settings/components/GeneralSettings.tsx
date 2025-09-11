import * as Ch from "@chakra-ui/react";
import SettingsGroup from "./shared/SettingsGroup";
import useRestoreSettings from "../hooks/useRestoreSettings";

export default function GeneralSettings() {
  const restoreSettingsMutation = useRestoreSettings();

  return (
    <SettingsGroup heading="General">
      <Ch.Field.Root>
        <Ch.Field.Label>Restore Defaults</Ch.Field.Label>
        <Ch.Field.HelperText>Restore the default settings.</Ch.Field.HelperText>
        <Ch.Button
          size={"xs"}
          colorPalette={"red"}
          marginTop={"2"}
          onClick={() => restoreSettingsMutation.mutate()}
        >
          Restore
        </Ch.Button>
      </Ch.Field.Root>
    </SettingsGroup>
  );
}
