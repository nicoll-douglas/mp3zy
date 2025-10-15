import { app } from "electron";
import path from "path";
import { promises as fs } from "fs";
import type { UserSettings } from "../../types/shared.js";
import logger from "./logger.js";

/**
 * Produces the default settings configuration for the application.
 *
 * @returns The default configuration object.
 */
async function defaultSettings(): Promise<UserSettings> {
  let defaultDownloadDir = app.getPath("music");

  try {
    await fs.access(defaultDownloadDir);
  } catch {
    defaultDownloadDir = app.getPath("home");
  }

  return {
    default_download_dir: defaultDownloadDir,
  };
}

/**
 * Gets the path to where the application settings file (settings.json) is saved.
 *
 * @returns The file path.
 */
function getSettingsPath(): string {
  const userDataPath = app.getPath("userData");

  return path.join(userDataPath, "settings.json");
}

/**
 * Overwrites the application settings file with a new settings configuration.
 *
 * @param settings The new settings configuration object.
 * @returns `true` if the file was successfully written to, `false` otherwise.
 */
async function setSettings(settings: UserSettings): Promise<boolean> {
  try {
    const settingsPath: string = getSettingsPath();
    const jsonString: string = JSON.stringify(settings, null, 2);

    await fs.writeFile(settingsPath, jsonString, "utf-8");

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
async function restoreSettings(): Promise<boolean> {
  logger.info("Restoring default settings...");

  const defaults: UserSettings = await defaultSettings();

  return setSettings(defaults);
}

/**
 * Retrieves the application's settings configuration object, or creates and returns if it doesn't exist yet.
 *
 * @returns The settings configuration object or `null` if the file couldn't be read.
 */
async function loadSettings(): Promise<UserSettings | null> {
  try {
    const settingsPath = getSettingsPath();
    const settingsData = await fs.readFile(settingsPath, "utf-8");

    return JSON.parse(settingsData);
  } catch (e: any) {
    if (e.code === "ENOENT") {
      const defaults = await defaultSettings();
      restoreSettings();

      return defaults;
    }

    logger.warn(`Failed to load settings file: ${e}`);

    return null;
  }
}

/**
 * Updates the settings file with updated or new configurations passed.
 *
 * @param updatedSettings New or updated configurations.
 * @returns `true` if the settings file was updated, `false` otherwise.
 */
async function updateSettings(
  updatedSettings: Partial<UserSettings>
): Promise<boolean> {
  logger.info("Updating settings...");

  const currentSettings = await loadSettings();

  if (!currentSettings) {
    logger.warn("Failed to update settings.");

    return false;
  }

  const newSettings: UserSettings = { ...currentSettings, ...updatedSettings };

  return setSettings(newSettings);
}

export { loadSettings, updateSettings, restoreSettings, defaultSettings };
