import { app } from "electron";
import path from "path";
import fs from "fs";
import defaultSettings from "../config/defaultSettings.js";
import type { UserSettings } from "../../types/shared.js";
import logger from "./logger.js";

/**
 * Gets the path to where the application settings file (settings.join) is saved.
 *
 * @returns The file path.
 */
function getSettingsPath() {
  const userDataPath = app.getPath("userData");
  return path.join(userDataPath, "settings.json");
}

/**
 * Synchronously overwrites the application settings file with a new settings configuration.
 *
 * @param settings The new settings configuration object.
 * @returns `true` if the file was successfully written to, `false` otherwise.
 */
function setSettings(settings: UserSettings): boolean {
  try {
    const settingsPath = getSettingsPath();
    fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2), "utf-8");

    logger.info("Successfully saved settings.");
    logger.debug(`Settings path: ${settingsPath}`);

    return true;
  } catch (e) {
    logger.warn(`Failed to write to settings file: ${e}`);

    return false;
  }
}

/**
 * Restores the application's default settings.
 *
 * @returns `true` if the settings file was written to, `false` otherwise.
 */
function restoreSettings(): boolean {
  logger.info("Restoring default settings...");

  return setSettings(defaultSettings());
}

/**
 * Retrieves the application's settings configuration object, or creates and returns if it doesn't exist yet.
 *
 * @returns The settings configuration object.
 */
function loadSettings(): UserSettings | null {
  const settingsPath = getSettingsPath();

  if (!fs.existsSync) {
    restoreSettings();
  }

  try {
    const settingsData = fs.readFileSync(settingsPath, "utf-8");

    return JSON.parse(settingsData);
  } catch (e) {
    logger.warn(`Failed to read settings file: ${e}`);

    return null;
  }
}

/**
 * Updates the settings file with updated or new configurations passed.
 *
 * @param updatedSettings New or updated configurations.
 * @returns `true` if the settings file was updated, `false` otherwise.
 */
function updateSettings(updatedSettings: Partial<UserSettings>): boolean {
  logger.info("Updating settings...");

  const currentSettings = loadSettings();

  if (!currentSettings) {
    logger.warn("Failed to update settings.");
    return false;
  }

  const newSettings = { ...currentSettings, ...updatedSettings };

  return setSettings(newSettings);
}

export { loadSettings, updateSettings, restoreSettings };
