import * as Ch from "@chakra-ui/react";
import { useDownloadFormContext } from "../../../context/DownloadFormContext";
import { Controller } from "react-hook-form";
import { useState } from "react";
import { LuFolder } from "react-icons/lu";

/**
 * Represents a file picker component that opens a dialog to let the user select the target output directory for their download.
 */
export default function DownloadDirectoryPicker() {
  const { form } = useDownloadFormContext();
  const [pickingDirectory, setPickingDirectory] = useState(false);

  return (
    <Ch.Field.Root
      maxW={"lg"}
      invalid={!!form.formState.errors.downloadDir}
      required
    >
      <Ch.Field.Label>
        Download Directory
        <Ch.Field.RequiredIndicator />
      </Ch.Field.Label>
      <Controller
        name="downloadDir"
        control={form.control}
        render={({ field }) => (
          <Ch.Group attached w="full">
            <Ch.Input
              {...field}
              disabled
              cursor={"default"}
              title={field.value}
              textOverflow={"ellipsis"}
              placeholder="Select directory"
            />
            <Ch.Button
              variant={"outline"}
              onClick={async () => {
                setPickingDirectory(true);

                const dir = await window.electronAPI.pickDirectory(
                  "Select Download Directory"
                );

                if (dir) {
                  form.setValue("downloadDir", dir);
                }

                setPickingDirectory(false);
              }}
              disabled={pickingDirectory}
            >
              <LuFolder /> Select
            </Ch.Button>
          </Ch.Group>
        )}
      />
      <Ch.Field.HelperText>
        The directory to download the track to.
      </Ch.Field.HelperText>
    </Ch.Field.Root>
  );
}
