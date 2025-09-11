import { BrowserWindow } from "electron";
import authWindowConfig from "../config/authWindow";

async function createAuthWindow() {
  const authWindow = new BrowserWindow(authWindowConfig);

  authWindow.webContents.on("will-redirect", (event, url) => {
    if (url.startsWith("")) {
      const searchParams = new URL(url).searchParams;
      const code = searchParams.get("code");
      const error = searchParams.get("error");
      console.log("code:", code);
      console.log("error", error);

      authWindow.close();
    }
  });
}

export { createAuthWindow };
