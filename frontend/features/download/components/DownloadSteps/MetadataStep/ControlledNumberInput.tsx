import { Controller } from "react-hook-form";
import * as Ch from "@chakra-ui/react";
import {
  type DownloadFormValidationRules,
  downloadFormValidationRuleset,
} from "../../../forms/downloadForm";
import { useDownloadFormContext } from "../../../context/DownloadFormContext";

/**
 * Props for the ControlledNumberInput component.
 */
export interface ControlledNumberInputProps {
  /**
   * The name of the field in the download form.
   */
  name: keyof typeof downloadFormValidationRuleset;

  /**
   * The text placeholder for the input element.
   */
  placeholder?: string;

  /**
   * The validation rules to pass to the controller.
   */
  rules?: DownloadFormValidationRules;
}

/**
 * Component that provides a controlled number input to use with the download form.
 */
export default function ControlledNumberInput({
  name,
  placeholder,
  rules,
}: ControlledNumberInputProps) {
  const { form } = useDownloadFormContext();

  return (
    <Controller
      name={name}
      control={form.control}
      rules={rules}
      render={({ field }) => (
        <Ch.NumberInput.Root
          disabled={field.disabled}
          name={field.name}
          value={field.value as string | undefined}
          onValueChange={({ value }) => field.onChange(value)}
        >
          <Ch.NumberInput.Control />
          <Ch.NumberInput.Input
            placeholder={placeholder}
            onBlur={field.onBlur}
          />
        </Ch.NumberInput.Root>
      )}
    />
  );
}
