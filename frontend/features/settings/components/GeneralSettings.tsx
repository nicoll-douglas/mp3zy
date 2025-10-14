import * as Ch from "@chakra-ui/react";
import SettingsGroup from "./shared/SettingsGroup";
import useRestoreSettings from "../hooks/useRestoreSettings";

/**
 * Represents a card component that holds general application settings.
 */
export default function GeneralSettings() {
  const restoreSettingsMutation = useRestoreSettings();

  // if error in update mutation, then toast error "failed to update settings"

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
