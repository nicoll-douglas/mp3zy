import * as Ch from "@chakra-ui/react";
import { useDownloadOptionsFormContext } from "../../../../context/DownloadOptionsFormContext";
import GeneralOptions from "./GeneralOptions";
import MetadataOptions from "./MetadataOptions";

export default function DownloadOptionsForm() {
  const { onFormSubmit, form } = useDownloadOptionsFormContext();

  return (
    <Ch.Card.Root size={"sm"}>
      <Ch.Card.Header>
        <Ch.Card.Title>Download Options</Ch.Card.Title>
        <Ch.Card.Description>Set download options.</Ch.Card.Description>
      </Ch.Card.Header>
      <Ch.Card.Body>
        <Ch.Stack gap={"5"} as={"form"} onSubmit={onFormSubmit} maxW={"lg"}>
          <GeneralOptions />
          <MetadataOptions />
          <Ch.Button loading={form.formState.isSubmitting} type="submit">
            Submit
          </Ch.Button>
        </Ch.Stack>
      </Ch.Card.Body>
    </Ch.Card.Root>
  );
}
