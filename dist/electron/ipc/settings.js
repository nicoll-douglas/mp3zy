import { ipcMain } from "electron";
import { loadSettings } from "../utils/settings.js";
ipcMain.handle("get-settings", async () => {
    return loadSettings();
});
