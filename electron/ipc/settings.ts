import { ipcMain } from "electron";
import { loadSettings } from "../utils/settings.js";

export default function registerSettingsHandlers() {
  ipcMain.handle("get-settings", async () => {
    return loadSettings();
  });
}
