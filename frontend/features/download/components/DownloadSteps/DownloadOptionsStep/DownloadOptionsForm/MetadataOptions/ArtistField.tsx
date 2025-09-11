import * as Ch from "@chakra-ui/react";
import type { FieldArrayWithId } from "react-hook-form";
import type { DownloadOptionsFormValues } from "../../../../../forms/downloadOptions";
import { useDownloadOptionsFormContext } from "../../../../../context/DownloadOptionsFormContext";
import { LuCircleMinus } from "react-icons/lu";

export default function ArtistField({
  field,
  index,
}: {
  field: FieldArrayWithId<DownloadOptionsFormValues, "artists", "id">;
  index: number;
}) {
  const { form, handleRemoveArtist } = useDownloadOptionsFormContext();

  return (
    <Ch.Field.Root key={field.id} required={index === 0}>
      <Ch.Field.Label>
        Artist {index + 1}
        <Ch.Show when={index === 0}>
          <Ch.Field.RequiredIndicator />
        </Ch.Show>
      </Ch.Field.Label>
      <Ch.HStack width={"full"}>
        <Ch.Group width={"full"}>
          <Ch.Input
            placeholder={index === 0 ? "Daft Punk" : `Artist ${index + 1}`}
            {...form.register(`artists.${index}.value`)}
          />
          <Ch.Show when={index > 0}>
            <Ch.Button
              onClick={handleRemoveArtist(index)}
              colorPalette={"red"}
              variant={"subtle"}
            >
              Remove
              <LuCircleMinus />
            </Ch.Button>
          </Ch.Show>
        </Ch.Group>
      </Ch.HStack>
    </Ch.Field.Root>
  );
}
