import * as Ch from "@chakra-ui/react";
import { useDownloadFormContext } from "../../../context/DownloadFormContext";
import { Controller } from "react-hook-form";
import { useState } from "react";
import { LuFolder, LuTrash } from "react-icons/lu";

/**
 * Represents a file picker component that opens a dialog to let the user select an album cover for their download.
 */
export default function AlbumCoverPicker() {
  const { form } = useDownloadFormContext();
  const [pickingFile, setPickingFile] = useState(false);

  return (
    <Ch.Field.Root maxW={"lg"} invalid={!!form.formState.errors.downloadDir}>
      <Ch.Field.Label>Album Cover</Ch.Field.Label>
      <Ch.Group w={"full"}>
        <Controller
          name="albumCoverPath"
          control={form.control}
          render={({ field }) => (
            <Ch.Group attached w="full">
              <Ch.Input
                {...field}
                disabled
                value={field.value ?? ""}
                cursor={"default"}
                title={field.value ?? ""}
                textOverflow={"ellipsis"}
              />
              <Ch.Button
                variant={"outline"}
                onClick={async () => {
                  setPickingFile(true);

                  const file =
                    await window.electronAPI.pickImageFile(
                      "Select Album Cover"
                    );

                  if (file) {
                    form.setValue("albumCoverPath", file);
                  }

                  setPickingFile(false);
                }}
                disabled={pickingFile}
              >
                <LuFolder /> Select
              </Ch.Button>
            </Ch.Group>
          )}
        />
        <Ch.IconButton
          colorPalette={"red"}
          variant={"surface"}
          onClick={() => form.setValue("albumCoverPath", "")}
        >
          <LuTrash />
        </Ch.IconButton>
      </Ch.Group>
    </Ch.Field.Root>
  );
}
