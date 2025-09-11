export default async function updateSavePath() {
  const newSaveDir = await window.electronAPI.pickSaveDirectory();
  if (!newSaveDir) return;
  await window.electronAPI.setSettings({ savePath: newSaveDir });
}
