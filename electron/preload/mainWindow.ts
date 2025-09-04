import { contextBridge, ipcRenderer } from "electron";
import { ElectronAPI } from "../../types/shared.js";

const electronAPI: ElectronAPI = {
  getSettings: () => ipcRenderer.invoke("get-settings"),
};

contextBridge.exposeInMainWorld("electronAPI", electronAPI);

console.log("Preload executed");
