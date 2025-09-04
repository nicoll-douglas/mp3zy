import fs from "fs";
import { app } from "electron";
import type { UserSettings } from "../../types/shared";
let savePath = app.getPath("music");

if (!fs.existsSync(savePath)) {
  savePath = app.getPath("home");
}

const defaultSettings: UserSettings = {
  savePath,
};

export default defaultSettings;
