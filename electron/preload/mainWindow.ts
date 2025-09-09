import { contextBridge, ipcRenderer } from "electron";
import { ElectronAPI, UserSettings } from "../../types/shared.js";

let backendAuthKey: string = "";

const electronAPI: ElectronAPI = {
  getSettings: () => ipcRenderer.invoke("get-settings"),
  setSettings: (updatedSettings: Partial<UserSettings>) =>
    ipcRenderer.invoke("set-settings", updatedSettings),
  pickSaveDirectory: () => ipcRenderer.invoke("pick-save-directory"),
  restoreSettings: () => ipcRenderer.invoke("restore-settings"),
  getBackendAuthKey: () => backendAuthKey,
};

ipcRenderer.on("set-backend-auth-key", (_, authKey) => {
  backendAuthKey = authKey;
});

contextBridge.exposeInMainWorld("electronAPI", electronAPI);
