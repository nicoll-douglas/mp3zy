import { Fieldset, Field, Show, Group } from "@chakra-ui/react";
import { downloadOptionsControlRules as rules } from "../../../../../forms/downloadOptions";
import ControlledNumberInput from "../shared/ControlledNumberInput";
import { useDownloadOptionsFormContext } from "../../../../../context/DownloadOptionsFormContext";

export default function ReleaseDateFieldset() {
  const { showMonthField, showDayField, form } =
    useDownloadOptionsFormContext();
  const errors = form.formState.errors;
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
              name="year"
              placeholder="2001"
              rules={rules["year"]}
            />
          </Field.Root>
          <Show when={showMonthField}>
            <Field.Root maxW={"fit"}>
              <Field.Label>Month</Field.Label>
              <ControlledNumberInput
                name="month"
                placeholder="3"
                rules={rules["month"]}
              />
            </Field.Root>
          </Show>
          <Show when={showDayField}>
            <Field.Root maxW={"fit"}>
              <Field.Label>Day</Field.Label>
              <ControlledNumberInput
                name="day"
                placeholder="12"
                rules={rules["day"]}
              />
            </Field.Root>
          </Show>
        </Group>
      </Fieldset.Content>
    </Fieldset.Root>
  );
}
