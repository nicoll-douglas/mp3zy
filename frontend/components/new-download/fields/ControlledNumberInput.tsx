import {
  Controller,
  type Control,
  type RegisterOptions,
} from "react-hook-form";
import { NumberInput } from "@chakra-ui/react";
import type { DownloadOptionsFormValues } from "../types";

export default function ControlledNumberInput({
  control,
  name,
  placeholder,
  min,
  max,
  rules,
}: {
  control: Control<DownloadOptionsFormValues, any, DownloadOptionsFormValues>;
  name: keyof DownloadOptionsFormValues;
  placeholder?: string;
  min?: number;
  max?: number;
  rules?: Omit<
    RegisterOptions<DownloadOptionsFormValues, keyof DownloadOptionsFormValues>,
    "valueAsNumber" | "valueAsDate" | "setValueAs" | "disabled"
  >;
}) {
  return (
    <Controller
      name={name}
      control={control}
      rules={rules}
      render={({ field }) => (
        <NumberInput.Root
          disabled={field.disabled}
          name={field.name}
          value={field.value as string | undefined}
          onValueChange={({ value }) => {
            field.onChange(value);
          }}
          min={min}
          max={max}
        >
          <NumberInput.Control />
          <NumberInput.Input placeholder={placeholder} onBlur={field.onBlur} />
        </NumberInput.Root>
      )}
    />
  );
}
