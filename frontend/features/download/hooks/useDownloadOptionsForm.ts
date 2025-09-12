import { useForm, useFieldArray } from "react-hook-form";
import { useEffect, useState } from "react";
import type { DownloadOptionsFormValues } from "../forms/downloadOptions";
import triggerDownload from "../services/triggerDownload";
import type { TriggerDownloadStatus } from "../types";

export default function useDownloadOptionsForm(audioUrl: string) {
  const [downloadStatus, setDownloadStatus] =
    useState<TriggerDownloadStatus | null>(null);

  const form = useForm<DownloadOptionsFormValues>({
    defaultValues: {
      codec: "mp3",
      artists: [{ value: "" }],
      bitrate: "320",
      trackNumber: "",
      discNumber: "",
      track: "",
      album: "",
      year: "",
      month: "",
      day: "",
    },
  });

  const { fields, append, remove } = useFieldArray({
    control: form.control,
    name: "artists",
  });

  const handleAddArtist = () => append({ value: "" });
  const handleRemoveArtist = (index: number) => () => remove(index);

  const codec = form.watch("codec");
  const year = form.watch("year");
  const month = form.watch("month");

  useEffect(() => {
    if (!year) {
      form.resetField("month");
    }
  }, [year]);

  useEffect(() => {
    if (!month) {
      form.resetField("day");
    }
  }, [month]);

  const onFormSubmit = form.handleSubmit(async (data) => {
    const result = await triggerDownload(audioUrl, data);
    setDownloadStatus(result.status);
  });

  return {
    downloadStatus,
    showBitrateField: codec === "mp3",
    showMonthField: !!year,
    showDayField: !!year && !!month,
    artistFields: fields,
    handleAddArtist,
    handleRemoveArtist,
    onFormSubmit,
    form,
  };
}
