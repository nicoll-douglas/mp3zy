import { Heading, Stack } from "@chakra-ui/react";
import { DownloadSteps } from "@/features/download";

export default function NewDownload() {
  return (
    <main>
      <Stack gap={"4"}>
        <Heading as={"h1"} size={"2xl"}>
          New Download
        </Heading>
        <DownloadSteps />
      </Stack>
    </main>
  );
}
