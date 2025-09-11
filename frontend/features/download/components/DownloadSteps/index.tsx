import { Steps, ButtonGroup, Button } from "@chakra-ui/react";
import { useState } from "react";
import { LuChevronLeft, LuChevronRight } from "react-icons/lu";
import {
  useAudioSearchContext,
  AudioSearchProvider,
} from "../../context/AudioSearchContext";
import SearchAudioStep from "./SearchAudioStep";

function DownloadStepsChild() {
  const [step, setStep] = useState(0);
  const { audioUrlSelected } = useAudioSearchContext();

  return (
    <Steps.Root step={step} onStepChange={(e) => setStep(e.step)} count={2}>
      <Steps.List>
        <Steps.Item index={0} title={"Search For Audio"}>
          <Steps.Indicator />
          <Steps.Title>Search For Audio</Steps.Title>
          <Steps.Separator />
        </Steps.Item>

        <Steps.Item index={1} title={"Download Options"}>
          <Steps.Indicator />
          <Steps.Title>Download Options</Steps.Title>
          <Steps.Separator />
        </Steps.Item>
      </Steps.List>

      <SearchAudioStep />

      <Steps.Content index={1}>
        {/* Download options step content */}
      </Steps.Content>

      <Steps.CompletedContent>All steps are complete!</Steps.CompletedContent>

      <ButtonGroup size="sm" variant="outline">
        <Steps.PrevTrigger asChild>
          <Button>
            <LuChevronLeft />
            Prev
          </Button>
        </Steps.PrevTrigger>

        <Steps.NextTrigger asChild>
          <Button disabled={step === 0 && !audioUrlSelected}>
            Next
            <LuChevronRight />
          </Button>
        </Steps.NextTrigger>
      </ButtonGroup>
    </Steps.Root>
  );
}

export default function DownloadSteps() {
  return (
    <AudioSearchProvider>
      <DownloadStepsChild />
    </AudioSearchProvider>
  );
}
