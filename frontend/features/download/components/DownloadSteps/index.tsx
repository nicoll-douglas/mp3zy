import * as Ch from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { LuChevronLeft, LuChevronRight } from "react-icons/lu";
import EnterUrlStep from "./EnterUrlStep";
import DownloadOptionsStep from "./DownloadOptionsStep";
import {
  DownloadFormProvider,
  useDownloadFormContext,
} from "../../context/DownloadFormContext";
import CompletedContent from "./CompletedContent";

export default function DownloadSteps() {
  const _DownloadSteps = () => {
    const [step, setStep] = useState(0);
    const { form } = useDownloadFormContext();

    const urlSelected = form.watch("url");

    useEffect(() => {
      if (form.formState.isSubmitSuccessful) {
        setStep(3);
      }
    }, [form.formState.isSubmitSuccessful]);

    return (
      <Ch.Steps.Root
        step={step}
        onStepChange={(e) => setStep(e.step)}
        count={2}
      >
        <Ch.Steps.List>
          <Ch.Steps.Item index={0} title={"Enter Source URL"}>
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

        <Ch.Steps.Content index={0}>
          <EnterUrlStep />
        </Ch.Steps.Content>

        <DownloadOptionsStep />
        <CompletedContent />

        <Ch.ButtonGroup size="sm" variant="outline">
          <Ch.Steps.PrevTrigger asChild>
            <Ch.Button disabled={step === 3 || step === 0}>
              <LuChevronLeft />
              Prev
            </Ch.Button>
          </Ch.Steps.PrevTrigger>

          <Ch.Steps.NextTrigger asChild>
            <Ch.Button disabled={!urlSelected && step === 0}>
              Next
              <LuChevronRight />
            </Ch.Button>
          </Ch.Steps.NextTrigger>
        </Ch.ButtonGroup>
      </Ch.Steps.Root>
    );
  };

  return (
    <DownloadFormProvider>
      <_DownloadSteps />
    </DownloadFormProvider>
  );
}
