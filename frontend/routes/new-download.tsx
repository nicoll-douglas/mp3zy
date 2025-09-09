import { Heading, Stack } from "@chakra-ui/react";
import NewDownloadSteps from "@/components/new-download/NewDownloadSteps";

export default function NewDownload() {
  return (
    <main>
      <Stack gap={"4"}>
        <Heading as={"h1"} size={"2xl"}>
          New Download
        </Heading>
        <NewDownloadSteps />
      </Stack>
    </main>
  );
}
