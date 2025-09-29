import type { UserSettings } from "types/shared";

export default async function getSettings(): Promise<UserSettings | null> {
  return window.electronAPI.getSettings();
}
