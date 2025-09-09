import { Controller, type Control } from "react-hook-form";
import { NumberInput } from "@chakra-ui/react";
import type { DownloadOptionsFormValues } from "../types";

export default function ControlledNumberInput({
  control,
  name,
  placeholder,
  min,
  max,
}: {
  control: Control<DownloadOptionsFormValues, any, DownloadOptionsFormValues>;
  name: keyof DownloadOptionsFormValues;
  placeholder?: string;
  min?: number;
  max?: number;
}) {
  return (
    <Controller
      name={name}
      control={control}
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
