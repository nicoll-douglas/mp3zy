import { ipcRenderer } from "electron";

let backendAuthKey: string = "";

function registerHandlers() {
  ipcRenderer.on("set-backend-auth-key", (_, authKey) => {
    backendAuthKey = authKey;
  });
}

const targets = {
  getBackendAuthKey: () => backendAuthKey,
};

export { registerHandlers, targets };
