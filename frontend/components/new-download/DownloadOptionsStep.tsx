import {
  Card,
  Heading,
  Steps,
  Stack,
  Box,
  Field,
  Input,
  NativeSelect,
  NumberInput,
  Show,
  Fieldset,
  For,
  HStack,
  Button,
  Group,
} from "@chakra-ui/react";
import { useForm, Controller, useFieldArray } from "react-hook-form";
import type { DownloadOptionsFormValues } from "./types";
import { LuCircleMinus, LuCirclePlus } from "react-icons/lu";
import ControlledNumberInput from "./fields/ControlledNumberInput";
import ReleaseDateFieldset from "./fields/ReleaseDateFieldset";

export default function DownloadOptionsStep({
  audioUrl,
}: {
  audioUrl: string | null;
}) {
  const {
    register,
    control,
    watch,
    setError,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<DownloadOptionsFormValues>({
    defaultValues: {
      codec: "mp3",
      artists: [{ value: "" }],
      bitrate: "320",
      trackNumber: "",
      discNumber: "",
      track: "",
      album: "",
      year: "",
      month: "",
      day: "",
    },
  });
  const { fields, append, remove } = useFieldArray({
    control,
    name: "artists",
  });
  const codec = watch("codec");
  const year = watch("year");
  const month = watch("month");

  const onSubmit = handleSubmit(async (data) => {
    const url = `${import.meta.env.VITE_BACKEND_URL}/download`;
    const res = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url: audioUrl, ...data }),
    });
    const body = await res.json();
  });

  return (
    <Steps.Content index={1}>
      <Stack gap={"4"}>
        <Card.Root size={"sm"}>
          <Card.Header>
            <Card.Title>Download Options</Card.Title>
            <Card.Description>Set download options.</Card.Description>
          </Card.Header>
          <Card.Body as={"form"}>
            <Stack gap={"5"}>
              <Box>
                <Heading as={"h3"} size={"md"} mb={"4"}>
                  General
                </Heading>
                <Stack gap={"5"} maxW={"lg"}>
                  <Field.Root invalid={!!errors.codec} required>
                    <Field.Label>
                      Desired Audio Codec
                      <Field.RequiredIndicator />
                    </Field.Label>
                    <NativeSelect.Root>
                      <NativeSelect.Field {...register("codec")}>
                        <option value="mp3">.mp3</option>
                        <option value="flac">.flac</option>
                      </NativeSelect.Field>
                      <NativeSelect.Indicator />
                    </NativeSelect.Root>
                    <Field.ErrorText>{errors.codec?.message}</Field.ErrorText>
                    <Field.HelperText>
                      The desired file output type.
                    </Field.HelperText>
                  </Field.Root>

                  <Show when={codec === "mp3"}>
                    <Field.Root invalid={!!errors.bitrate} required>
                      <Field.Label>
                        Bitrate <Field.RequiredIndicator />
                      </Field.Label>
                      <NativeSelect.Root>
                        <NativeSelect.Field {...register("bitrate")}>
                          <option value="128">128 kB/s</option>
                          <option value="192">192 kB/s</option>
                          <option value="320">320 kB/s</option>
                        </NativeSelect.Field>
                        <NativeSelect.Indicator />
                      </NativeSelect.Root>
                      <Field.ErrorText>
                        {errors.bitrate?.message}
                      </Field.ErrorText>
                      <Field.HelperText>
                        The higher the bitrate, the better the audio quality.
                      </Field.HelperText>
                    </Field.Root>
                  </Show>
                </Stack>
              </Box>

              <Box>
                <Heading as={"h3"} size={"md"} mb={"4"}>
                  Metadata
                </Heading>
                <Stack maxW={"lg"} gap="5">
                  <Fieldset.Root>
                    <Fieldset.Legend>Artists</Fieldset.Legend>
                    <Fieldset.ErrorText>
                      {errors.artists?.message}
                    </Fieldset.ErrorText>
                    <Fieldset.Content>
                      <For each={fields}>
                        {(field, index) => (
                          <Field.Root key={field.id} required={index === 0}>
                            <Field.Label>
                              Artist {index + 1}
                              <Show when={index === 0}>
                                <Field.RequiredIndicator />
                              </Show>
                            </Field.Label>
                            <HStack width={"full"}>
                              <Group width={"full"}>
                                <Input
                                  placeholder={
                                    index === 0
                                      ? "Daft Punk"
                                      : `Artist ${index + 1}`
                                  }
                                  {...register(`artists.${index}.value`)}
                                />
                                <Show when={index > 0}>
                                  <Button
                                    onClick={() => remove(index)}
                                    colorPalette={"red"}
                                    variant={"subtle"}
                                  >
                                    Remove
                                    <LuCircleMinus />
                                  </Button>
                                </Show>
                              </Group>
                            </HStack>
                          </Field.Root>
                        )}
                      </For>
                      <Button
                        maxW={"fit"}
                        onClick={() => append({ value: "" })}
                        variant={"subtle"}
                      >
                        Add <LuCirclePlus />
                      </Button>
                    </Fieldset.Content>
                  </Fieldset.Root>

                  <Field.Root invalid={!!errors.track} required>
                    <Field.Label>
                      Track Name <Field.RequiredIndicator />
                    </Field.Label>
                    <Input placeholder="One More Time" {...register("track")} />
                    <Field.ErrorText>{errors.track?.message}</Field.ErrorText>
                  </Field.Root>

                  <Field.Root>
                    <Field.Label>Album Name</Field.Label>
                    <Input placeholder="Discovery" {...register("album")} />
                    <Field.ErrorText>{errors.album?.message}</Field.ErrorText>
                  </Field.Root>
                  <Field.Root invalid={!!errors.trackNumber}>
                    <Field.Label>Track Number</Field.Label>
                    <ControlledNumberInput
                      control={control}
                      name="trackNumber"
                      placeholder="1"
                    />
                    <Field.ErrorText>
                      {errors.trackNumber?.message}
                    </Field.ErrorText>
                    <Field.HelperText>
                      The track's number in the disc or album.
                    </Field.HelperText>
                  </Field.Root>

                  <Field.Root invalid={!!errors.discNumber}>
                    <Field.Label>Disc Number</Field.Label>
                    <ControlledNumberInput
                      control={control}
                      name="discNumber"
                      placeholder="1"
                    />
                    <Field.ErrorText>
                      {errors.discNumber?.message}
                    </Field.ErrorText>
                    <Field.HelperText>
                      The album disc the track is on (usually 1).
                    </Field.HelperText>
                  </Field.Root>

                  <ReleaseDateFieldset
                    year={year}
                    month={month}
                    control={control}
                    errors={errors}
                  />

                  <Button loading={isSubmitting} type="submit">
                    Submit
                  </Button>
                </Stack>
              </Box>
            </Stack>
          </Card.Body>
        </Card.Root>
      </Stack>
    </Steps.Content>
  );
}
