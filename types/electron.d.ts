import type { ElectronAPI } from "./shared";

declare global {
  interface Window {
    electronAPI: ElectronAPI;
  }
}
