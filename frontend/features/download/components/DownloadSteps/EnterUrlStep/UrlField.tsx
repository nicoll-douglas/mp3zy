import { useDownloadFormContext } from "@/features/download/context/DownloadFormContext";
import * as Ch from "@chakra-ui/react";
import { Controller } from "react-hook-form";

/**
 * Represents a card component that holds the URL field of what the user selects or types.
 */
export default function UrlField() {
  const { form } = useDownloadFormContext();

  return (
    <Ch.Card.Root size={"sm"}>
      <Ch.Card.Header>
        <Ch.Card.Title>URL</Ch.Card.Title>
        <Ch.Card.Description>
          Manually enter a URL or search and select below.
        </Ch.Card.Description>
      </Ch.Card.Header>
      <Ch.Card.Body>
        <Ch.Field.Root
          invalid={!!form.formState.errors.url}
          maxW={"lg"}
          required
        >
          <Ch.Field.Label>
            URL
            <Ch.Field.RequiredIndicator />
          </Ch.Field.Label>
          <Controller
            name="url"
            control={form.control}
            render={({ field }) => <Ch.Input {...field} />}
          />
          <Ch.Field.ErrorText>
            {form.formState.errors.url?.message}
          </Ch.Field.ErrorText>
        </Ch.Field.Root>
      </Ch.Card.Body>
    </Ch.Card.Root>
  );
}
