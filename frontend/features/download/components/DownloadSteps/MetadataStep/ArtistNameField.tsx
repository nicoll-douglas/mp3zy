import * as Ch from "@chakra-ui/react";
import { useDownloadFormContext } from "../../../context/DownloadFormContext";
import { LuCircleMinus } from "react-icons/lu";

/**
 * Props for the ArtistNameField component.
 */
export interface ArtistNameFieldProps {
  /**
   * The index of the field in the artist name field array.
   */
  index: number;
}

/**
 * Represents a field for the user to enter an artist name associated with a track.
 *
 * The user is able to remove the field from view if the artist index is greater than 0.
 */
export default function ArtistNameField({ index }: ArtistNameFieldProps) {
  const { form, utils } = useDownloadFormContext();

  return (
    <Ch.Field.Root required={index === 0}>
      <Ch.Field.Label>
        Artist {index + 1}
        <Ch.Show when={index === 0}>
          <Ch.Field.RequiredIndicator />
        </Ch.Show>
      </Ch.Field.Label>

      <Ch.Group width={"full"}>
        <Ch.Input
          placeholder={`Artist ${index + 1}`}
          {...form.register(`artistNames.${index}.value`)}
        />
        <Ch.Show when={index > 0}>
          <Ch.IconButton
            onClick={() => utils.removeArtistName(index)}
            colorPalette={"red"}
            variant={"surface"}
            aria-label={`Remove Artist ${index + 1}`}
          >
            <LuCircleMinus />
          </Ch.IconButton>
        </Ch.Show>
      </Ch.Group>
    </Ch.Field.Root>
  );
}
