import { contextBridge, ipcRenderer } from "electron";
import type { ElectronAPI, UserSettings } from "../../types/shared.js";

let backendAuthKey: string = "";

// The API object to be exposed on the window object in the renderer process
const electronAPI: ElectronAPI = {
  getSettings: async () => ipcRenderer.invoke("get-settings"),
  setSettings: async (updatedSettings: Partial<UserSettings>) =>
    ipcRenderer.invoke("set-settings", updatedSettings),
  pickSaveDirectory: async () => ipcRenderer.invoke("pick-save-directory"),
  restoreSettings: async () => ipcRenderer.invoke("restore-settings"),
  getBackendAuthKey: () => backendAuthKey,
};

ipcRenderer.on("set-backend-auth-key", (_, authKey) => {
  backendAuthKey = authKey;
});

contextBridge.exposeInMainWorld("electronAPI", electronAPI);
