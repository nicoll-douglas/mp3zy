import * as Ch from "@chakra-ui/react";
import DownloadOptionsForm from "./DownloadOptionsForm";

export default function DownloadOptionsStep() {
  return (
    <Ch.Steps.Content index={1}>
      <Ch.Stack gap={"4"}>
        <DownloadOptionsForm />
      </Ch.Stack>
    </Ch.Steps.Content>
  );
}
