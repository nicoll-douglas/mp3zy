import { ipcMain } from "electron";
import { loadSettings } from "../utils/settings";

ipcMain.handle("get-settings", async () => {
  return loadSettings();
});
