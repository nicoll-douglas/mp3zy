const { app } = require("electron");
const path = require("path");
const fs = require("fs");
const defaultSettings = require("../config/defaultSettings.js");

function getSettingsPath() {
  const userDataPath = app.getPath("userData");
  return path.join(userDataPath, "settings.json");
}

function loadSettings() {
  const settingsPath = getSettingsPath();

  if (fs.existsSync(settingsPath)) {
    return JSON.parse(fs.readFileSync(settingsPath, "utf-8"));
  }

  saveSettings(defaultSettings);
  return defaultSettings;
}

function saveSettings(data) {
  const settingsPath = getSettingsPath();
  fs.writeFileSync(settingsPath, JSON.stringify(data, null, 2), "utf-8");
  console.log(`Settings saved.`);
}

module.exports = { loadSettings, saveSettings };
