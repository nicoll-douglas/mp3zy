import { ipcMain } from "electron";
import { pickDirectory, pickImageFile } from "../services/dialog.js";
import { IpcChannels } from "./channels.js";

/**
 * Registers the dialog-related IPC handlers.
 */
function registerHandlers() {
  ipcMain.handle(IpcChannels.pickDirectory, async (_, dialogTitle: string) =>
    pickDirectory(dialogTitle)
  );

  ipcMain.handle(IpcChannels.pickImageFile, async (_, dialogTitle: string) =>
    pickImageFile(dialogTitle)
  );
}

export { registerHandlers };
