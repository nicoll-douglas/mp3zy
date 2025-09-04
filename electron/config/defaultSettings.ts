import fs from "fs";
import { app } from "electron";
import type { UserSettings } from "../../types/shared.ts";

function defaultSettings() {
  let savePath = app.getPath("music");

  if (!fs.existsSync(savePath)) {
    savePath = app.getPath("home");
  }

  const value: UserSettings = {
    savePath,
  };

  return value;
}

export default defaultSettings;
