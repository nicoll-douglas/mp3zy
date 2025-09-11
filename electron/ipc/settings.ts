import { ipcMain, ipcRenderer, dialog } from "electron";
import {
  loadSettings,
  updateSettings,
  restoreSettings,
} from "../services/settings.js";
import type { UserSettings } from "../../types/shared.js";

function registerHandlers() {
  ipcMain.handle("get-settings", async () => {
    return loadSettings();
  });

  ipcMain.handle(
    "set-settings",
    async (_event, settings: Partial<UserSettings>) => {
      return updateSettings(settings);
    }
  );

  ipcMain.handle("pick-save-directory", async () => {
    const result = await dialog.showOpenDialog({
      properties: ["openDirectory"],
      title: "Select a New Save Directory",
    });

    return result.canceled ? null : result.filePaths[0];
  });

  ipcMain.handle("restore-settings", async () => {
    return restoreSettings();
  });
}

const targets = {
  getSettings: () => ipcRenderer.invoke("get-settings"),
  setSettings: (updatedSettings: Partial<UserSettings>) =>
    ipcRenderer.invoke("set-settings", updatedSettings),
  pickSaveDirectory: () => ipcRenderer.invoke("pick-save-directory"),
  restoreSettings: () => ipcRenderer.invoke("restore-settings"),
};

export { registerHandlers };
