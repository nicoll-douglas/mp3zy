import {
  Card,
  Field,
  Stack,
  Input,
  Steps,
  Text,
  Button,
  Image,
  HStack,
  VStack,
  Box,
  Link,
  Flex,
  RadioCard,
  Show,
  For,
  EmptyState,
} from "@chakra-ui/react";
import { LuChevronRight, LuSearch, LuSearchX } from "react-icons/lu";
import { useForm } from "react-hook-form";
import type { SearchAudioFormValues, YtDlpAudioSearchResult } from "./types";
import { useState, type Dispatch, type SetStateAction } from "react";

export default function SearchAudioStep({
  audioUrlSelected,
  setAudioUrlSelected,
}: {
  audioUrlSelected: string | null;
  setAudioUrlSelected: Dispatch<SetStateAction<string | null>>;
}) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting, isSubmitted },
  } = useForm<SearchAudioFormValues>();
  const [searchResults, setSearchResults] = useState<YtDlpAudioSearchResult[]>(
    []
  );

  const onSubmit = handleSubmit(async (data) => {
    const queryString = new URLSearchParams({ ...data }).toString();
    const res = await fetch(
      `${import.meta.env.VITE_BACKEND_URL}/audio-search/yt-dlp?${queryString}`
    );
    const body = await res.json();
    setSearchResults(body);
  });

  return (
    <Steps.Content index={0}>
      <Stack gap={"4"}>
        <Card.Root size={"sm"}>
          <Card.Header>
            <Card.Title>Song Details</Card.Title>
            <Card.Description>
              Input the details for the song you wish to search for.
            </Card.Description>
          </Card.Header>
          <Card.Body as={"form"} onSubmit={onSubmit}>
            <Stack gap={"5"} maxW={"lg"}>
              <Field.Root invalid={!!errors.artist} required>
                <Field.Label>
                  Main Artist
                  <Field.RequiredIndicator />
                </Field.Label>
                <Input placeholder="e.g Daft Punk" {...register("artist")} />
                <Field.ErrorText>{errors.artist?.message}</Field.ErrorText>
              </Field.Root>
              <Field.Root invalid={!!errors.track} required>
                <Field.Label>
                  Song Name
                  <Field.RequiredIndicator />
                </Field.Label>
                <Input placeholder="e.g One More Time" {...register("track")} />
                <Field.ErrorText>{errors.track?.message}</Field.ErrorText>
              </Field.Root>
              <Button
                type="submit"
                variant={"subtle"}
                maxW={"fit"}
                loading={isSubmitting}
              >
                Search
                <LuSearch />
              </Button>
            </Stack>
          </Card.Body>
        </Card.Root>
        <Show when={isSubmitted}>
          <Card.Root size={"sm"}>
            <Card.Header>
              <Card.Title>Results</Card.Title>
              <Card.Description>{`${searchResults.length} total.`}</Card.Description>
            </Card.Header>
            <Card.Body>
              <Stack gap={"4"}>
                <RadioCard.Root
                  value={audioUrlSelected}
                  onValueChange={(e) => setAudioUrlSelected(e.value)}
                >
                  <RadioCard.Label>Select Source for Audio</RadioCard.Label>
                  <For
                    each={searchResults}
                    fallback={
                      <EmptyState.Root>
                        <EmptyState.Content>
                          <EmptyState.Indicator>
                            <LuSearchX />
                          </EmptyState.Indicator>
                          <VStack textAlign="center">
                            <EmptyState.Title>No results</EmptyState.Title>
                            <EmptyState.Description>
                              Try adjusting your search.
                            </EmptyState.Description>
                          </VStack>
                        </EmptyState.Content>
                      </EmptyState.Root>
                    }
                  >
                    {(item, index) => (
                      <RadioCard.Item key={index} value={item.url} width="full">
                        <RadioCard.ItemHiddenInput />
                        <RadioCard.ItemControl>
                          <HStack gap={"4"}>
                            <RadioCard.ItemIndicator />
                            <RadioCard.ItemContent>
                              <Flex gap={"4"}>
                                <Image
                                  src={item.thumbnails[0].url}
                                  width={180}
                                  borderRadius={"sm"}
                                />
                                <Box>
                                  <RadioCard.ItemText>
                                    {item.title}
                                  </RadioCard.ItemText>
                                  <Text>{item.channel}</Text>
                                  <Link href={item.url}>{item.url}</Link>
                                </Box>
                              </Flex>
                            </RadioCard.ItemContent>
                          </HStack>
                        </RadioCard.ItemControl>
                      </RadioCard.Item>
                    )}
                  </For>
                </RadioCard.Root>
              </Stack>
            </Card.Body>
            <Card.Footer flexDir={"column"} alignItems={"start"}>
              <Text>
                Can't find the video you're looking for? Try downloading with a
                link directly.
              </Text>
              <Button size={"xs"}>
                Go
                <LuChevronRight />
              </Button>
            </Card.Footer>
          </Card.Root>
        </Show>
      </Stack>
    </Steps.Content>
  );
}
