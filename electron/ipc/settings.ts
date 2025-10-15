import { ipcMain } from "electron";
import {
  loadSettings,
  updateSettings,
  restoreSettings,
} from "../services/settings.js";
import type { UserSettings } from "../../types/shared.js";
import { IpcChannels } from "./channels.js";

/**
 * Registers the settings-related IPC handlers.
 */
function registerHandlers() {
  ipcMain.handle(IpcChannels.getSettings, async () => loadSettings());

  ipcMain.handle(
    IpcChannels.updateSettings,
    async (_, settings: Partial<UserSettings>) => updateSettings(settings)
  );

  ipcMain.handle(IpcChannels.restoreSettings, async () => restoreSettings());
}

export { registerHandlers };
