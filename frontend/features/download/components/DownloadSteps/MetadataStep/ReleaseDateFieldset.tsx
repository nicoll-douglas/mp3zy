import { Fieldset, Field, Show, Group } from "@chakra-ui/react";
import { downloadFormValidationRuleset } from "../../../forms/downloadForm";
import ControlledNumberInput from "./ControlledNumberInput";
import { useDownloadFormContext } from "../../../context/DownloadFormContext";

/**
 * Component that represents a fieldset for the user to enter release date metadata for a track.
 */
export default function ReleaseDateFieldset() {
  const { form, utils } = useDownloadFormContext();
  const errors = form.formState.errors;
  const error = errors.releaseYear ?? errors.releaseMonth ?? errors.releaseDay;

  return (
    <Fieldset.Root invalid={!!error}>
      <Fieldset.Legend>Release Date</Fieldset.Legend>
      <Fieldset.Content>
        <Group alignItems={"end"}>
          <Field.Root maxW={"fit"}>
            <Field.Label>Year</Field.Label>
            <ControlledNumberInput
              name="releaseYear"
              placeholder="2001"
              rules={downloadFormValidationRuleset.releaseYear}
            />
          </Field.Root>
          <Field.Root maxW={"fit"}>
            <Field.Label>Month</Field.Label>
            <ControlledNumberInput
              name="releaseMonth"
              placeholder="3"
              rules={downloadFormValidationRuleset.releaseMonth}
            />
          </Field.Root>
          <Field.Root maxW={"fit"}>
            <Field.Label>Day</Field.Label>
            <ControlledNumberInput
              name="releaseDay"
              placeholder="12"
              rules={downloadFormValidationRuleset.releaseDay}
            />
          </Field.Root>
        </Group>
      </Fieldset.Content>
      <Fieldset.ErrorText>{error?.message}</Fieldset.ErrorText>
    </Fieldset.Root>
  );
}
