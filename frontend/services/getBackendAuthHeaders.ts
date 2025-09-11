export default function getBackendAuthHeaders() {
  const authKey = window.electronAPI.getBackendAuthKey();
  const headers = {
    "X-Electron-Auth": authKey,
  };
  return headers;
}
