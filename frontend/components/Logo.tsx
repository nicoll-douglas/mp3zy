import { system } from "@/config/theme";

export default function Logo() {
  return (
    <svg
      width={system.token("spacing.5")}
      height={system.token("spacing.5")}
      viewBox="0 0 88 88"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M47.5 16.5L44 24.5L22 18.5L50 52L76.5 68L71.5 46L78 16L54.5 23.5L58.5 42.5L44 24.5L47.5 16.5L88 5L79 46L88 83L44 58L0 5L47.5 16.5Z"
        fill="currentColor"
      />
    </svg>
  );
}
