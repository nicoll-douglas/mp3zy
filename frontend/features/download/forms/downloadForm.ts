import type { RegisterOptions } from "react-hook-form";
import type { TrackBitrate, TrackCodec } from "../types";

/**
 * Represents the form field names and types in the download form.
 */
interface DownloadFormValues {
  artistNames: Array<{ value: string }>;
  trackName: string;
  codec: TrackCodec;
  bitrate: TrackBitrate;
  albumName: string;
  trackNumber: string;
  discNumber: string;
  releaseYear: string;
  releaseMonth: string;
  releaseDay: string;
  downloadDir: string;
  url: string;
  albumCoverPath: string | null;
}

type DownloadFormValidationRule = Omit<
  RegisterOptions<DownloadFormValues, keyof DownloadFormValues>,
  "setValueAs" | "disabled" | "valueAsNumber" | "valueAsDate"
>;

/**
 * Represents validation rules to pass to the download form when registering fields.
 */
const downloadFormValidationRules: {
  [key: string]: DownloadFormValidationRule;
} = {
  trackNumber: {
    required: false,
    validate: {
      isPositive: (v: string | { value: string }[] | null) => {
        if (!v) return true;

        return (
          parseFloat(v as string) > 0 || "Track number must be greater than 0"
        );
      },
      isInteger: (v: string | { value: string }[] | null) => {
        if (!v) return true;

        return (
          /^[0-9]*$/.test(v as string) || "Track number must be an integer"
        );
      },
    },
  },
  discNumber: {
    required: false,
    validate: {
      isPositive: (v: string | { value: string }[] | null) => {
        if (!v) return true;

        return (
          parseFloat(v as string) > 0 || "Disc number must be greater than 0"
        );
      },
      isInteger: (v: string | { value: string }[] | null) => {
        if (!v) return true;

        return /^[0-9]*$/.test(v as string) || "Disc number must be an integer";
      },
    },
  },
  releaseYear: {
    required: false,
    validate: {
      isZeroOrGreater: (v: string | { value: string }[] | null) => {
        if (!v) return true;

        return (
          parseFloat(v as string) >= 0 ||
          "Year must be greater than or equal to 0"
        );
      },
      isInteger: (v: string | { value: string }[] | null) => {
        if (!v) return true;

        return /^[0-9]*$/.test(v as string) || "Year must be an integer";
      },
      isYear: (v: string | { value: string }[] | null) => {
        if (!v) return true;

        return (
          parseFloat(v as string) <= 9999 || "Year must be no greater than 9999"
        );
      },
    },
  },
  releaseMonth: {
    required: false,
    validate: {
      isPositive: (v: string | { value: string }[] | null) => {
        if (!v) return true;

        return parseFloat(v as string) > 0 || "Month must be greater than 0";
      },
      isInteger: (v: string | { value: string }[] | null) => {
        if (!v) return true;

        return /^[0-9]*$/.test(v as string) || "Month must be an integer";
      },
      isMonth: (v: string | { value: string }[] | null) => {
        if (!v) return true;

        return (
          parseFloat(v as string) <= 12 || "Month must be no greater than 12"
        );
      },
    },
  },
  releaseDay: {
    required: false,
    validate: {
      isPositive: (v: string | { value: string }[] | null) => {
        if (!v) return true;

        return parseFloat(v as string) > 0 || "Day must be greater than 0";
      },
      isInteger: (v: string | { value: string }[] | null) => {
        if (!v) return true;

        return /^[0-9]*$/.test(v as string) || "Day must be an integer";
      },
      isDay: (v: string | { value: string }[] | null) => {
        if (!v) return true;

        return (
          parseFloat(v as string) <= 31 || "Day must be no greater than 31"
        );
      },
    },
  },
};

export { downloadFormValidationRules, type DownloadFormValues };
