import { contextBridge, ipcRenderer } from "electron";
import { ElectronAPI, UserSettings } from "../../types/shared.js";

const electronAPI: ElectronAPI = {
  getSettings: () => ipcRenderer.invoke("get-settings"),
  setSettings: (updatedSettings: Partial<UserSettings>) =>
    ipcRenderer.invoke("set-settings", updatedSettings),
  pickSaveDirectory: () => ipcRenderer.invoke("pick-save-directory"),
  restoreSettings: () => ipcRenderer.invoke("restore-settings"),
};

contextBridge.exposeInMainWorld("electronAPI", electronAPI);
