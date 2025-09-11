import * as Ch from "@chakra-ui/react";
import { LuSearch } from "react-icons/lu";
import { useAudioSearchContext } from "../../../context/AudioSearchContext";

export default function SearchForm() {
  const { form, onFormSubmit } = useAudioSearchContext();

  return (
    <Ch.Card.Root size={"sm"}>
      <Ch.Card.Header>
        <Ch.Card.Title>Song Details</Ch.Card.Title>
        <Ch.Card.Description>
          Input the details for the song you wish to search for.
        </Ch.Card.Description>
      </Ch.Card.Header>
      <Ch.Card.Body>
        <Ch.Stack as={"form"} onSubmit={onFormSubmit} gap={"5"} maxW={"lg"}>
          <Ch.Field.Root invalid={!!form.formState.errors.artist} required>
            <Ch.Field.Label>
              Main Artist
              <Ch.Field.RequiredIndicator />
            </Ch.Field.Label>
            <Ch.Input
              placeholder="e.g Daft Punk"
              {...form.register("artist")}
            />
            <Ch.Field.ErrorText>
              {form.formState.errors.artist?.message}
            </Ch.Field.ErrorText>
          </Ch.Field.Root>
          <Ch.Field.Root invalid={!!form.formState.errors.track} required>
            <Ch.Field.Label>
              Song Name
              <Ch.Field.RequiredIndicator />
            </Ch.Field.Label>
            <Ch.Input
              placeholder="e.g One More Time"
              {...form.register("track")}
            />
            <Ch.Field.ErrorText>
              {form.formState.errors.track?.message}
            </Ch.Field.ErrorText>
          </Ch.Field.Root>
          <Ch.Button
            type="submit"
            variant={"subtle"}
            maxW={"fit"}
            loading={form.formState.isSubmitting}
          >
            Search
            <LuSearch />
          </Ch.Button>
        </Ch.Stack>
      </Ch.Card.Body>
    </Ch.Card.Root>
  );
}
