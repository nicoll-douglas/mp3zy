import { useDownloadOptionsFormContext } from "@/features/download/context/DownloadFormContext";
import * as Ch from "@chakra-ui/react";
import OptionsGroup from "./shared/OptionsGroup";

export default function GeneralOptions() {
  const { form, showBitrateField } = useDownloadOptionsFormContext();

  return (
    <OptionsGroup heading="General">
      <Ch.Field.Root invalid={!!form.formState.errors.codec} required>
        <Ch.Field.Label>
          Desired Audio Codec
          <Ch.Field.RequiredIndicator />
        </Ch.Field.Label>
        <Ch.NativeSelect.Root>
          <Ch.NativeSelect.Field {...form.register("codec")}>
            <option value="mp3">.mp3</option>
            <option value="flac">.flac</option>
          </Ch.NativeSelect.Field>
          <Ch.NativeSelect.Indicator />
        </Ch.NativeSelect.Root>
        <Ch.Field.ErrorText>
          {form.formState.errors.codec?.message}
        </Ch.Field.ErrorText>
        <Ch.Field.HelperText>The desired file output type.</Ch.Field.HelperText>
      </Ch.Field.Root>

      <Ch.Show when={showBitrateField}>
        <Ch.Field.Root invalid={!!form.formState.errors.bitrate} required>
          <Ch.Field.Label>
            Bitrate <Ch.Field.RequiredIndicator />
          </Ch.Field.Label>
          <Ch.NativeSelect.Root>
            <Ch.NativeSelect.Field {...form.register("bitrate")}>
              <option value="128">128 kB/s</option>
              <option value="192">192 kB/s</option>
              <option value="320">320 kB/s</option>
            </Ch.NativeSelect.Field>
            <Ch.NativeSelect.Indicator />
          </Ch.NativeSelect.Root>
          <Ch.Field.ErrorText>
            {form.formState.errors.bitrate?.message}
          </Ch.Field.ErrorText>
          <Ch.Field.HelperText>
            The higher the bitrate, the better the audio quality.
          </Ch.Field.HelperText>
        </Ch.Field.Root>
      </Ch.Show>
    </OptionsGroup>
  );
}
