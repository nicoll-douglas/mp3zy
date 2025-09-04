import { BrowserWindow } from "electron";
import mainWindowConfig from "../config/mainWindow.js";
import path from "path";
import { fileURLToPath } from "url";
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
function createMainWindow() {
    const mainWindow = new BrowserWindow(mainWindowConfig);
    if (process.env.APP_ENV === "development") {
        mainWindow.once("ready-to-show", () => {
            mainWindow.showInactive();
            mainWindow.minimize();
        });
        mainWindow.loadURL("http://127.0.0.1:5173");
    }
    else {
        mainWindow.loadFile(path.join(__dirname, "../../dist/frontend/index.html"));
    }
}
export { createMainWindow };
