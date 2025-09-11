import * as Ch from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { LuChevronLeft, LuChevronRight } from "react-icons/lu";
import {
  useAudioSearchContext,
  AudioSearchProvider,
} from "../../context/AudioSearchContext";
import SearchAudioStep from "./SearchAudioStep";
import DownloadOptionsStep from "./DownloadOptionsStep";
import {
  DownloadOptionsFormProvider,
  useDownloadOptionsFormContext,
} from "../../context/DownloadOptionsFormContext";
import CompletedContent from "./CompletedContent";

export default function DownloadSteps() {
  const __DownloadSteps = () => {
    const [step, setStep] = useState(0);
    const { audioUrlSelected } = useAudioSearchContext();
    const { form } = useDownloadOptionsFormContext();

    useEffect(() => {
      if (form.formState.isSubmitSuccessful) {
        setStep(2);
      }
    }, [form.formState.isSubmitSuccessful]);

    return (
      <Ch.Steps.Root
        step={step}
        onStepChange={(e) => setStep(e.step)}
        count={2}
      >
        <Ch.Steps.List>
          <Ch.Steps.Item index={0} title={"Search For Audio"}>
            <Ch.Steps.Indicator />
            <Ch.Steps.Title>Search For Audio</Ch.Steps.Title>
            <Ch.Steps.Separator />
          </Ch.Steps.Item>

          <Ch.Steps.Item index={1} title={"Download Options"}>
            <Ch.Steps.Indicator />
            <Ch.Steps.Title>Download Options</Ch.Steps.Title>
            <Ch.Steps.Separator />
          </Ch.Steps.Item>
        </Ch.Steps.List>

        <SearchAudioStep />
        <DownloadOptionsStep />
        <CompletedContent />

        <Ch.ButtonGroup size="sm" variant="outline">
          <Ch.Steps.PrevTrigger asChild>
            <Ch.Button disabled={step === 2}>
              <LuChevronLeft />
              Prev
            </Ch.Button>
          </Ch.Steps.PrevTrigger>

          <Ch.Steps.NextTrigger asChild>
            <Ch.Button
              disabled={
                (step === 0 && !audioUrlSelected) || step === 1 || step === 2
              }
            >
              Next
              <LuChevronRight />
            </Ch.Button>
          </Ch.Steps.NextTrigger>
        </Ch.ButtonGroup>
      </Ch.Steps.Root>
    );
  };

  const _DownloadSteps = () => {
    const { audioUrlSelected } = useAudioSearchContext();

    return (
      <DownloadOptionsFormProvider audioUrl={audioUrlSelected as string}>
        <__DownloadSteps />
      </DownloadOptionsFormProvider>
    );
  };

  return (
    <AudioSearchProvider>
      <_DownloadSteps />
    </AudioSearchProvider>
  );
}
