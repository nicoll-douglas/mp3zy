import dotenv from "dotenv";
dotenv.config();

import { app, BrowserWindow } from "electron";
import path from "path";

import { createMainWindow } from "./windows/mainWindow.js";
import {
  startBackend,
  killBackend,
  watchBackend,
} from "./processes/backend.js";
import registerSettingsHandlers from "./ipc/settings.js";

app.whenReady().then(() => {
  startBackend();
  if (process.env.APP_ENV === "development") {
    watchBackend();
  }
  createMainWindow();
  registerSettingsHandlers();
});

app.on("will-quit", () => {
  killBackend();
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createMainWindow();
  }
});
