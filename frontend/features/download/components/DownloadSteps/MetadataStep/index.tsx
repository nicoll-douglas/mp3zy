import { useDownloadFormContext } from "../../../context/DownloadFormContext";
import * as Ch from "@chakra-ui/react";
import { LuCirclePlus, LuDownload } from "react-icons/lu";
import ArtistNameField from "./ArtistNameField";
import ControlledNumberInput from "./ControlledNumberInput";
import { downloadFormValidationRuleset } from "../../../forms/downloadForm";
import ReleaseDateFieldset from "./ReleaseDateFieldset";
import AlbumCoverPicker from "./AlbumCoverPicker";

/**
 * Represents a card component that lays out the step for the user to configure metadata options for their download such as track name, artists, etc.
 *
 * Since this is the last step, contains a submit button in order for the user to start the download.
 */
export default function MetadataStep() {
  const { form, utils, onFormSubmit } = useDownloadFormContext();

  return (
    <Ch.Card.Root size={"sm"}>
      <Ch.Card.Header>
        <Ch.Card.Title>Track Metadata</Ch.Card.Title>
      </Ch.Card.Header>
      <Ch.Card.Body>
        <Ch.Stack gap={"5"} maxW={"lg"} as={"form"} onSubmit={onFormSubmit}>
          <Ch.Fieldset.Root>
            <Ch.Fieldset.Legend>Artists</Ch.Fieldset.Legend>

            <Ch.Fieldset.ErrorText>
              {form.formState.errors.artistNames?.message}
            </Ch.Fieldset.ErrorText>

            <Ch.Fieldset.Content>
              <Ch.For each={utils.artistNameFields}>
                {(field, index) => (
                  <ArtistNameField key={field.id} index={index} />
                )}
              </Ch.For>

              <Ch.Button
                maxW={"fit"}
                onClick={utils.addArtistName}
                variant={"subtle"}
              >
                Add <LuCirclePlus />
              </Ch.Button>
            </Ch.Fieldset.Content>
          </Ch.Fieldset.Root>

          <Ch.Field.Root invalid={!!form.formState.errors.trackName} required>
            <Ch.Field.Label>
              Track Name <Ch.Field.RequiredIndicator />
            </Ch.Field.Label>
            <Ch.Input
              placeholder="One More Time"
              {...form.register("trackName")}
            />
            <Ch.Field.ErrorText>
              {form.formState.errors.trackName?.message}
            </Ch.Field.ErrorText>
          </Ch.Field.Root>

          <Ch.Field.Root>
            <Ch.Field.Label>Album Name</Ch.Field.Label>
            <Ch.Input placeholder="Discovery" {...form.register("albumName")} />
            <Ch.Field.ErrorText>
              {form.formState.errors.albumName?.message}
            </Ch.Field.ErrorText>
          </Ch.Field.Root>

          <AlbumCoverPicker />

          <Ch.Field.Root invalid={!!form.formState.errors.trackNumber}>
            <Ch.Field.Label>Track Number</Ch.Field.Label>
            <ControlledNumberInput
              name="trackNumber"
              placeholder="1"
              rules={downloadFormValidationRuleset.trackNumber}
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
              rules={downloadFormValidationRuleset.discNumber}
            />
            <Ch.Field.ErrorText>
              {form.formState.errors.discNumber?.message}
            </Ch.Field.ErrorText>
            <Ch.Field.HelperText>
              The album disc the track is on.
            </Ch.Field.HelperText>
          </Ch.Field.Root>

          <ReleaseDateFieldset />

          <Ch.Button
            type="submit"
            variant={"subtle"}
            maxW={"fit"}
            loading={form.formState.isSubmitting}
          >
            Start Download
            <LuDownload />
          </Ch.Button>
        </Ch.Stack>
      </Ch.Card.Body>
    </Ch.Card.Root>
  );
}
