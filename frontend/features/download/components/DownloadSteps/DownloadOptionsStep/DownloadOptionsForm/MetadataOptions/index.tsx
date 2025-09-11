import { useDownloadOptionsFormContext } from "../../../../../context/DownloadOptionsFormContext";
import * as Ch from "@chakra-ui/react";
import { LuCirclePlus } from "react-icons/lu";
import ArtistField from "./ArtistField";
import OptionsGroup from "../shared/OptionsGroup";
import ControlledNumberInput from "../shared/ControlledNumberInput";
import { downloadOptionsControlRules as rules } from "../../../../../forms/downloadOptions";
import ReleaseDateFieldset from "./ReleaseDateFieldset";

export default function MetadataOptions() {
  const { form, artistFields, handleAddArtist } =
    useDownloadOptionsFormContext();

  return (
    <OptionsGroup heading="Metadata">
      <Ch.Fieldset.Root>
        <Ch.Fieldset.Legend>Artists</Ch.Fieldset.Legend>
        <Ch.Fieldset.ErrorText>
          {form.formState.errors.artists?.message}
        </Ch.Fieldset.ErrorText>
        <Ch.Fieldset.Content>
          <Ch.For each={artistFields}>
            {(field, index) => <ArtistField key={field.id} index={index} />}
          </Ch.For>
          <Ch.Button maxW={"fit"} onClick={handleAddArtist} variant={"subtle"}>
            Add <LuCirclePlus />
          </Ch.Button>
        </Ch.Fieldset.Content>
      </Ch.Fieldset.Root>

      <Ch.Field.Root invalid={!!form.formState.errors.track} required>
        <Ch.Field.Label>
          Track Name <Ch.Field.RequiredIndicator />
        </Ch.Field.Label>
        <Ch.Input placeholder="One More Time" {...form.register("track")} />
        <Ch.Field.ErrorText>
          {form.formState.errors.track?.message}
        </Ch.Field.ErrorText>
      </Ch.Field.Root>

      <Ch.Field.Root>
        <Ch.Field.Label>Album Name</Ch.Field.Label>
        <Ch.Input placeholder="Discovery" {...form.register("album")} />
        <Ch.Field.ErrorText>
          {form.formState.errors.album?.message}
        </Ch.Field.ErrorText>
      </Ch.Field.Root>

      <Ch.Field.Root invalid={!!form.formState.errors.trackNumber}>
        <Ch.Field.Label>Track Number</Ch.Field.Label>
        <ControlledNumberInput
          name="trackNumber"
          placeholder="1"
          rules={rules["trackNumber"]}
        />
        <Ch.Field.ErrorText>
          {form.formState.errors.trackNumber?.message}
        </Ch.Field.ErrorText>
        <Ch.Field.HelperText>
          The track's number in the disc or album.
        </Ch.Field.HelperText>
      </Ch.Field.Root>

      <Ch.Field.Root invalid={!!form.formState.errors.discNumber}>
        <Ch.Field.Label>Disc Number</Ch.Field.Label>
        <ControlledNumberInput
          name="discNumber"
          placeholder="1"
          rules={rules["discNumber"]}
        />
        <Ch.Field.ErrorText>
          {form.formState.errors.discNumber?.message}
        </Ch.Field.ErrorText>
        <Ch.Field.HelperText>
          The album disc the track is on (usually 1).
        </Ch.Field.HelperText>
      </Ch.Field.Root>

      <ReleaseDateFieldset />
    </OptionsGroup>
  );
}
