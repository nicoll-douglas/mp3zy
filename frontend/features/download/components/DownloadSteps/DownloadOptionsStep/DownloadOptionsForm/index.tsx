import * as Ch from "@chakra-ui/react";
import { useDownloadOptionsFormContext } from "../../../../context/DownloadOptionsFormContext";
import GeneralOptions from "./GeneralOptions";
import MetadataOptions from "./MetadataOptions";

export default function DownloadOptionsForm() {
  const { onFormSubmit } = useDownloadOptionsFormContext();

  return (
    <Ch.Card.Root size={"sm"}>
      <Ch.Card.Header>
        <Ch.Card.Title>Download Options</Ch.Card.Title>
        <Ch.Card.Description>Set download options.</Ch.Card.Description>
      </Ch.Card.Header>
      <Ch.Card.Body>
        <Ch.Stack gap={"5"} as={"form"} onSubmit={onFormSubmit}>
          <GeneralOptions />
          <MetadataOptions />
        </Ch.Stack>
      </Ch.Card.Body>
    </Ch.Card.Root>
  );
}
