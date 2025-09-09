import { Steps, ButtonGroup, Button } from "@chakra-ui/react";
import DownloadOptionsStep from "./DownloadOptionsStep";
import SearchAudioStep from "./SearchAudioStep";
import { useState } from "react";
import { LuChevronLeft, LuChevronRight } from "react-icons/lu";

export default function NewDownloadSteps() {
  const [step, setStep] = useState(0);
  const [audioUrlSelected, setAudioUrlSelected] = useState<string | null>(null);

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
      <SearchAudioStep
        audioUrlSelected={audioUrlSelected}
        setAudioUrlSelected={setAudioUrlSelected}
      />
      <DownloadOptionsStep audioUrl={audioUrlSelected} />
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
