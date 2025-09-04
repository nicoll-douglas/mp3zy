import fs from "fs";
import { app } from "electron";
function defaultSettings() {
    let savePath = app.getPath("music");
    if (!fs.existsSync(savePath)) {
        savePath = app.getPath("home");
    }
    const value = {
        savePath,
    };
    return value;
}
export default defaultSettings;
