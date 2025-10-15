import {
  useForm,
  useFieldArray,
  type UseFormReturn,
  type FieldArrayWithId,
} from "react-hook-form";
import { useEffect, useState, type BaseSyntheticEvent } from "react";
import type { DownloadFormValues } from "../forms/downloadForm";
import startDownload from "../services/startDownload";
import type { PostDownloadsResponse } from "../types";
import { useGetSettings } from "@/features/settings";

/**
 * Return type of the useDownloadForm hook.
 */
export interface UseDownloadFormReturn {
  /**
   * The response to the form submission request if submitted.
   */
  response: PostDownloadsResponse | null;

  /**
   * The form submission handler.
   */
  onFormSubmit: (
    e?: BaseSyntheticEvent<object, any, any> | undefined
  ) => Promise<void>;

  /**
   * The form.
   */
  form: UseFormReturn<DownloadFormValues, any, DownloadFormValues>;

  /**
   * Utilities for form rendering.
   */
  utils: {
    /**
     * A boolean indicating whether to show the bitrate field if applicable to a codec selected.
     */
    showBitrateField: boolean;

    /**
     * A boolean indicating whether to show the release month field if the release year field is non-empty.
     */
    showMonthField: boolean;

    /**
     * A boolean indicating whether to show the release day field if the release year and month fields are non-empty.
     */
    showDayField: boolean;

    /**
     * The artist name field array.
     */
    artistNameFields: FieldArrayWithId<
      DownloadFormValues,
      "artistNames",
      "id"
    >[];

    /**
     * A helper function to add an artist name to the field array.
     */
    addArtistName: () => void;

    /**
     * A helper function to remove an artist name from the field array.
     */
    removeArtistName: (index: number) => void;
  };
}

/**
 * Hook to provide a form that uses the start downloads service on submission as well as related functions and values.
 *
 * @returns The form and related functions and values.
 */
export default function useDownloadForm(): UseDownloadFormReturn {
  const [response, setResponse] = useState<PostDownloadsResponse | null>(null);
  const getSettingsQuery = useGetSettings();
  const defaultDownloadDir = getSettingsQuery?.data?.default_download_dir;

  const form = useForm<DownloadFormValues>({
    defaultValues: {
      codec: "mp3",
      artistNames: [{ value: "" }],
      bitrate: "320",
      trackNumber: "",
      discNumber: "",
      trackName: "",
      albumName: "",
      releaseYear: "",
      releaseMonth: "",
      releaseDay: "",
      downloadDir: defaultDownloadDir ?? "",
      url: "",
      albumCoverPath: "",
    },
  });

  useEffect(() => {
    if (defaultDownloadDir) {
      form.setValue("downloadDir", defaultDownloadDir);
    }
  }, [defaultDownloadDir]);

  const { fields, append, remove } = useFieldArray({
    control: form.control,
    name: "artistNames",
  });

  const addArtistName = () => append({ value: "" });
  const removeArtistName = (index: number) => remove(index);

  const codec = form.watch("codec");
  const releaseYear = form.watch("releaseYear");
  const releaseMonth = form.watch("releaseMonth");

  useEffect(() => {
    if (!releaseYear) {
      form.resetField("releaseMonth");
    }
  }, [releaseYear]);

  useEffect(() => {
    if (!releaseMonth) {
      form.resetField("releaseDay");
    }
  }, [releaseMonth]);

  const onFormSubmit = form.handleSubmit(async (data) => {
    const res = await startDownload(data);
    setResponse(res);
  });

  return {
    response,
    onFormSubmit,
    form,
    utils: {
      showBitrateField: codec === "mp3",
      showMonthField: !!releaseYear,
      showDayField: !!releaseYear && !!releaseMonth,
      artistNameFields: fields,
      addArtistName,
      removeArtistName,
    },
  };
}
