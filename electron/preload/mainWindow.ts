import { contextBridge, ipcRenderer } from "electron";
import type { ElectronAPI, UserSettings } from "../../types/shared.js";
import { IpcChannels } from "../ipc/channels.js";

// The API object to be exposed on the window object in the renderer process
const electronAPI: ElectronAPI = {
  getSettings: async () => ipcRenderer.invoke(IpcChannels.getSettings),

  updateSettings: async (updatedSettings: Partial<UserSettings>) =>
    ipcRenderer.invoke(IpcChannels.updateSettings, updatedSettings),

  pickDirectory: async (dialogTitle: string) =>
    ipcRenderer.invoke(IpcChannels.pickDirectory, dialogTitle),

  pickImageFile: async (dialogTitle: string) =>
    ipcRenderer.invoke(IpcChannels.pickImageFile, dialogTitle),

  restoreSettings: async () => ipcRenderer.invoke(IpcChannels.restoreSettings),
};

contextBridge.exposeInMainWorld("electronAPI", electronAPI);
