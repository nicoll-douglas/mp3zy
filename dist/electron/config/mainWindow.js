import path from "path";
import { fileURLToPath } from "url";
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const mainWindowConfig = {
    width: 1000,
    height: 800,
    show: process.env.APP_ENV !== "development",
    webPreferences: {
        contextIsolation: true,
        nodeIntegration: false,
        preload: path.join(__dirname, "../preload/mainWindow.ts"),
    },
};
export default mainWindowConfig;
