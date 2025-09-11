import { Controller, type RegisterOptions } from "react-hook-form";
import * as Ch from "@chakra-ui/react";
import type { DownloadOptionsFormValues } from "../../../../../forms/downloadOptions";
import { useDownloadOptionsFormContext } from "../../../../../context/DownloadOptionsFormContext";

export default function ControlledNumberInput({
  name,
  placeholder,
  rules,
}: {
  name: keyof DownloadOptionsFormValues;
  placeholder?: string;
  rules?: Omit<
    RegisterOptions<DownloadOptionsFormValues, keyof DownloadOptionsFormValues>,
    "valueAsNumber" | "valueAsDate" | "setValueAs" | "disabled"
  >;
}) {
  const { form } = useDownloadOptionsFormContext();

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
          onValueChange={({ value }) => {
            field.onChange(value);
          }}
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
