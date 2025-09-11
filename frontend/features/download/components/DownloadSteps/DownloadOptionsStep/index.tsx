import * as Ch from "@chakra-ui/react";
import { useAudioSearchContext } from "@/features/download/context/AudioSearchContext";
import DownloadOptionsForm from "./DownloadOptionsForm";
import { DownloadOptionsFormProvider } from "../../../context/DownloadOptionsFormContext";

export default function DownloadOptionsStep() {
  const { audioUrlSelected } = useAudioSearchContext();

  return (
    <Ch.Steps.Content index={1}>
      <Ch.Stack gap={"4"}>
        <DownloadOptionsFormProvider audioUrl={audioUrlSelected as string}>
          <DownloadOptionsForm />
        </DownloadOptionsFormProvider>
      </Ch.Stack>
    </Ch.Steps.Content>
  );
}
