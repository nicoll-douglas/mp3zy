import { dialog } from "electron";

/**
 * Opens a dialog for the user to pick a directory.
 *
 * @param dialogTitle The title of the dialog.
 * @returns The first file path selected, or `null` if the dialog was canceled.
 */
async function pickDirectory(dialogTitle: string): Promise<string | null> {
  const result = await dialog.showOpenDialog({
    properties: ["openDirectory"],
    title: dialogTitle,
  });

  return result.canceled ? null : result.filePaths[0];
}

/**
 * Opens a dialog for the user to pick a single image file.
 *
 * @param dialogTitle The title of the dialog.
 * @returns The first file selected, or `null` if the dialog was canceled.
 */
async function pickImageFile(dialogTitle: string): Promise<string | null> {
  const result = await dialog.showOpenDialog({
    title: dialogTitle,
    buttonLabel: "Select",
    properties: ["openFile"],
    filters: [{ name: "Images", extensions: ["jpg", "jpeg", "png"] }],
  });

  return result.canceled ? null : result.filePaths[0];
}

export { pickDirectory, pickImageFile };
