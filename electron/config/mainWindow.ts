import { BrowserWindowConstructorOptions } from "electron";
import path from "path";

// configuration for the window where the main application runs
const mainWindowConfig: BrowserWindowConstructorOptions = {
  width: 1000,
  height: 800,
  show: process.env.APP_ENV !== "development",
  webPreferences: {
    contextIsolation: true,
    nodeIntegration: false,
    preload: path.join(__dirname, "../preload/mainWindow.js"),
  },
};

export default mainWindowConfig;
