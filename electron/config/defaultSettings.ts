import fs from "fs";
import { app } from "electron";
import type { UserSettings } from "../../types/shared.ts";

/**
 * Produces the default settings configuration for the application.
 *
 * @returns The default configuration object.
 */
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
