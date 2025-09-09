import { Fieldset, Field, Show, Group } from "@chakra-ui/react";
import { type Control, type FieldErrors } from "react-hook-form";
import { type DownloadOptionsFormValues } from "../types";
import ControlledNumberInput from "./ControlledNumberInput";
import { controlRules } from "../validation";

export default function ReleaseDateFieldset({
  year,
  month,
  control,
  errors,
}: {
  control: Control<DownloadOptionsFormValues, any, DownloadOptionsFormValues>;
  year: string;
  month: string;
  errors: FieldErrors<DownloadOptionsFormValues>;
}) {
  let error;

  if (errors.year) {
    error = errors.year.message;
  } else if (errors.month) {
    error = errors.month.message;
  } else if (errors.day) {
    error = errors.day.message;
  }

  return (
    <Fieldset.Root invalid={!!error}>
      <Fieldset.Legend>Release Date</Fieldset.Legend>
      <Fieldset.ErrorText>{error}</Fieldset.ErrorText>
      <Fieldset.Content>
        <Group alignItems={"end"}>
          <Field.Root maxW={"fit"}>
            <Field.Label>Year</Field.Label>
            <ControlledNumberInput
              control={control}
              name="year"
              placeholder="2001"
              rules={controlRules["year"]}
            />
          </Field.Root>
          <Show when={!!year}>
            <Field.Root maxW={"fit"}>
              <Field.Label>Month</Field.Label>
              <ControlledNumberInput
                control={control}
                name="month"
                placeholder="3"
                rules={controlRules["month"]}
              />
            </Field.Root>
          </Show>
          <Show when={!!year && !!month}>
            <Field.Root maxW={"fit"}>
              <Field.Label>Day</Field.Label>
              <ControlledNumberInput
                control={control}
                name="day"
                placeholder="12"
                rules={controlRules["day"]}
              />
            </Field.Root>
          </Show>
        </Group>
      </Fieldset.Content>
    </Fieldset.Root>
  );
}
