import { app } from "electron";
import path from "path";
import fs from "fs";
import defaultSettings from "../config/defaultSettings.js";
import type { UserSettings } from "../../types/shared.ts";

function getSettingsPath() {
  const userDataPath = app.getPath("userData");
  return path.join(userDataPath, "settings.json");
}

function loadSettings(): UserSettings {
  const settingsPath = getSettingsPath();

  if (fs.existsSync(settingsPath)) {
    return JSON.parse(fs.readFileSync(settingsPath, "utf-8"));
  }

  const defaults = defaultSettings();
  saveSettings(defaults);

  return defaults;
}

function saveSettings(data: UserSettings) {
  const settingsPath = getSettingsPath();
  fs.writeFileSync(settingsPath, JSON.stringify(data, null, 2), "utf-8");
  console.log(`Settings saved.`);
}

export { loadSettings, saveSettings };
