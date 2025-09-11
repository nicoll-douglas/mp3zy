import { contextBridge } from "electron";
import { ElectronAPI } from "../../types/shared.js";
import { targets as settingsIpcTargets } from "../ipc/settings.js";
import { targets as backendAuthIpcTargets } from "../ipc/backendAuth.js";

const electronAPI: ElectronAPI = {
  ...settingsIpcTargets,
  ...backendAuthIpcTargets,
};

contextBridge.exposeInMainWorld("electronAPI", electronAPI);
