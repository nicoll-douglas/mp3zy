export interface UserSettings {
  savePath: string;
}

export interface ElectronAPI {
  getSettings: () => Promise<UserSettings | null>;
  updateSettings: (updatedSettings: Partial<UserSettings>) => Promise<boolean>;
  pickSaveDirectory: () => Promise<string | null>;
  restoreSettings: () => Promise<boolean>;
  getBackendAuthKey: () => string;
}
