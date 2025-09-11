import type { RegisterOptions } from "react-hook-form";

interface DownloadOptionsFormValues {
  artists: Array<{ value: string }>;
  track: string;
  album: string;
  codec: "mp3" | "flac";
  trackNumber: string;
  discNumber: string;
  bitrate: "128" | "192" | "320";
  year: string;
  month: string;
  day: string;
}

type DownloadOptionsFieldControlRules = Omit<
  RegisterOptions<DownloadOptionsFormValues, keyof DownloadOptionsFormValues>,
  "setValueAs" | "disabled" | "valueAsNumber" | "valueAsDate"
>;

const isPositive = (v: string | { value: string }[], label: string) =>
  parseFloat(v as string) > 0 || `${label} must be greater than 0`;

const isInteger = (v: string | { value: string }[], label: string) =>
  /^[0-9]*$/.test(v as string) || `${label} must be an integer`;

const downloadOptionsControlRules: {
  [key: string]: DownloadOptionsFieldControlRules;
} = {
  trackNumber: {
    required: false,
    validate: {
      isPositive: (v: string | { value: string }[]) => {
        if (!v) return true;
        return isPositive(v, "Track number");
      },
      isInteger: (v: string | { value: string }[]) => {
        if (!v) return true;
        return isInteger(v, "Track number");
      },
    },
  },
  discNumber: {
    required: false,
    validate: {
      isPositive: (v: string | { value: string }[]) => {
        if (!v) return true;
        return isPositive(v, "Disc number");
      },
      isInteger: (v: string | { value: string }[]) => {
        if (!v) return true;
        return isInteger(v, "Disc number");
      },
    },
  },
  year: {
    required: false,
    validate: {
      isPositive: (v: string | { value: string }[]) => {
        if (!v) return true;
        return isPositive(v, "Year");
      },
      isInteger: (v: string | { value: string }[]) => {
        if (!v) return true;
        return isInteger(v, "Year");
      },
      isYear: (v: string | { value: string }[]) => {
        if (!v) return true;
        const currentYear = new Date().getFullYear();
        return (
          parseFloat(v as string) <= currentYear ||
          `Year must be no greater than ${currentYear}`
        );
      },
    },
  },
  month: {
    required: false,
    validate: {
      isPositive: (v: string | { value: string }[]) => {
        if (!v) return true;
        return isPositive(v, "Month");
      },
      isInteger: (v: string | { value: string }[]) => {
        if (!v) return true;
        return isInteger(v, "Month");
      },
      isMonth: (v: string | { value: string }[]) => {
        if (!v) return true;
        return (
          parseFloat(v as string) <= 12 || "Month must be no greater than 12"
        );
      },
    },
  },
  day: {
    required: false,
    validate: {
      isPositive: (v: string | { value: string }[]) => {
        if (!v) return true;
        return isPositive(v, "Day");
      },
      isInteger: (v: string | { value: string }[]) => {
        if (!v) return true;
        return isInteger(v, "Day");
      },
      isDay: (v: string | { value: string }[]) => {
        if (!v) return true;
        return (
          parseFloat(v as string) <= 31 || "Day must be no greater than 31"
        );
      },
    },
  },
};

export { downloadOptionsControlRules, type DownloadOptionsFormValues };
