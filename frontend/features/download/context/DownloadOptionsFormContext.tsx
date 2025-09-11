import { createContext, useContext, type ReactNode } from "react";
import useDownloadOptionsForm from "../hooks/useDownloadOptionsForm";
import type { UseFormReturn, FieldArrayWithId } from "react-hook-form";
import type { DownloadOptionsFormValues } from "../forms/downloadOptions";

type DownloadOptionsFormContextValue = {
  taskId: string | null;
  showBitrateField: boolean;
  showMonthField: boolean;
  showDayField: boolean;
  artistFields: FieldArrayWithId<DownloadOptionsFormValues, "artists", "id">[];
  handleAddArtist: () => void;
  handleRemoveArtist: (index: number) => () => void;
  onFormSubmit: (e?: React.BaseSyntheticEvent) => Promise<void>;
  form: UseFormReturn<
    DownloadOptionsFormValues,
    any,
    DownloadOptionsFormValues
  >;
} | null;

export const DownloadOptionsFormContext =
  createContext<DownloadOptionsFormContextValue>(null);

export function DownloadOptionsFormProvider({
  children,
  audioUrl,
}: {
  children: ReactNode;
  audioUrl: string;
}) {
  const downloadOptionsForm = useDownloadOptionsForm(audioUrl);

  return (
    <DownloadOptionsFormContext value={downloadOptionsForm}>
      {children}
    </DownloadOptionsFormContext>
  );
}

export function useDownloadOptionsFormContext() {
  const value = useContext(DownloadOptionsFormContext);

  if (value === null) {
    throw new Error(
      "useContext must be used within context provider (DownloadOptionsFormContext"
    );
  }

  return value;
}
