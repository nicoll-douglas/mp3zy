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
import MetadataStep from "./MetadataStep";

/**
 * Represents a step-based flow of configuring a track download and then submitting to start it.
 */
export default function DownloadSteps() {
  const _DownloadSteps = () => {
    const [step, setStep] = useState(0);
    const { form } = useDownloadFormContext();

    const url = form.watch("url");

    const prevDisabled = step === 3 || step === 0;
    const nextDisabled = (step === 0 && !url) || step >= 2;

    useEffect(() => {
      if (form.formState.isSubmitSuccessful) {
        setStep(3);
      }
    }, [form.formState.isSubmitSuccessful]);

    return (
      <Ch.Steps.Root
        step={step}
        onStepChange={(e) => setStep(e.step)}
        count={3}
      >
        <Ch.Steps.List>
          <Ch.Steps.Item index={0} title={"Enter Source URL"}>
            <Ch.Steps.Indicator />
            <Ch.Steps.Title>Enter Source URL</Ch.Steps.Title>
            <Ch.Steps.Separator />
          </Ch.Steps.Item>

          <Ch.Steps.Item index={1} title={"Set Download Options"}>
            <Ch.Steps.Indicator />
            <Ch.Steps.Title>Set Download Options</Ch.Steps.Title>
            <Ch.Steps.Separator />
          </Ch.Steps.Item>

          <Ch.Steps.Item index={2} title={"Set Track Metadata"}>
            <Ch.Steps.Indicator />
            <Ch.Steps.Title>Set Track Metadata</Ch.Steps.Title>
            <Ch.Steps.Separator />
          </Ch.Steps.Item>
        </Ch.Steps.List>

        <Ch.Steps.Content index={0}>
          <EnterUrlStep />
        </Ch.Steps.Content>

        <Ch.Steps.Content index={1}>
          <DownloadOptionsStep />
        </Ch.Steps.Content>

        <Ch.Steps.Content index={2}>
          <MetadataStep />
        </Ch.Steps.Content>

        <Ch.Steps.CompletedContent>
          <CompletedContent />
        </Ch.Steps.CompletedContent>

        <Ch.ButtonGroup size="sm" variant="outline">
          <Ch.Steps.PrevTrigger asChild>
            <Ch.Button disabled={prevDisabled}>
              <LuChevronLeft />
              Prev
            </Ch.Button>
          </Ch.Steps.PrevTrigger>

          <Ch.Steps.NextTrigger asChild>
            <Ch.Button disabled={nextDisabled}>
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
