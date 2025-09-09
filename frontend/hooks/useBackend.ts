export default function useBackend() {
  const authKey = window.electronAPI.getBackendAuthKey();
  const headers = {
    "X-Electron-Auth": authKey,
  };
  return { headers };
}
