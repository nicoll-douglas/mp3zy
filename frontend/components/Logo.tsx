import { system } from "@/config/theme";

export default function Logo() {
  return (
    <svg
      width={system.token("spacing.5")}
      height={system.token("spacing.5")}
      viewBox="0 0 88 88"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M47.5 16.5L44 24.5L22 18.5L62 64.5L77 16.5L54.5 23.5L58.5 42.5L44 24.5L47.5 16.5L88 5L66 83L0 5L47.5 16.5Z"
        fill="currentColor"
      />
    </svg>
  );
}
