import { BrowserWindow } from "electron";
import mainWindowConfig from "../config/mainWindow.js";
import path from "path";

/**
 * Creates the main application window with the respective configuration.
 *
 * @param backendAuthKey The backend authentication key that the renderer will receive.
 */
function createMainWindow(backendAuthKey: string) {
  const mainWindow = new BrowserWindow(mainWindowConfig);

  if (process.env.APP_ENV === "development") {
    mainWindow.once("ready-to-show", () => {
      mainWindow.showInactive();
      mainWindow.minimize();
    });

    mainWindow.loadURL(String(process.env.VITE_APP_URL));
  } else {
    mainWindow.loadFile(path.join(__dirname, "../../frontend/index.html"));
  }

  mainWindow.webContents.on("did-finish-load", () => {
    mainWindow.webContents.send("set-backend-auth-key", backendAuthKey);
  });
}

export { createMainWindow };
