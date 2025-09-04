import { app } from "electron";
import path from "path";
import fs from "fs";
import defaultSettings from "../config/defaultSettings.js";
import type { UserSettings } from "../../types/shared.ts";

function getSettingsPath() {
  const userDataPath = app.getPath("userData");
  return path.join(userDataPath, "settings.json");
}

function setSettings(settings: UserSettings) {
  const settingsPath = getSettingsPath();
  fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2), "utf-8");
  console.log(`Settings saved (${settingsPath}).`);
}

function restoreSettings() {
  setSettings(defaultSettings());
}

function loadSettings(): UserSettings {
  const settingsPath = getSettingsPath();

  if (fs.existsSync(settingsPath)) {
    return JSON.parse(fs.readFileSync(settingsPath, "utf-8"));
  }

  const defaults = defaultSettings();
  setSettings(defaults);

  return defaults;
}

function updateSettings(updatedSettings: Partial<UserSettings>) {
  const currentSettings = loadSettings();
  const newSettings = { ...currentSettings, ...updatedSettings };
  setSettings(newSettings);
}

export { loadSettings, updateSettings, restoreSettings };
