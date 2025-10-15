/**
 * Represents the names of different IPC channels in the application.
 */
export enum IpcChannels {
  getSettings = "settings:get",
  updateSettings = "settings:update",
  restoreSettings = "settings:restore",

  pickDirectory = "dialog:pick-dir",
  pickImageFile = "dialog:pick-img",
}
