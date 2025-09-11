import dotenv from "dotenv";
dotenv.config();

import { app, BrowserWindow } from "electron";

import { createMainWindow } from "./windows/mainWindow.js";
import {
  startBackend,
  killBackend,
  watchBackend,
} from "./processes/backend.js";
import { registerHandlers as registerSettingsIpcHandlers } from "./ipc/settings.js";
import generateAuthKey from "./utils/generateAuthKey.js";

const backendAuthKey = generateAuthKey();

app.whenReady().then(() => {
  startBackend(backendAuthKey);
  if (process.env.APP_ENV === "development") {
    watchBackend(backendAuthKey);
  }
  createMainWindow(backendAuthKey);
  registerSettingsIpcHandlers();
});

app.on("will-quit", () => {
  killBackend();
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createMainWindow(backendAuthKey);
  }
});
