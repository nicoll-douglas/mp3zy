export interface UserSettings {
  savePath: string;
}

export interface ElectronAPI {
  getSettings: () => Promise<UserSettings>;
  setSettings: (updatedSettings: Partial<UserSettings>) => Promise<void>;
  pickSaveDirectory: () => Promise<string | null>;
  restoreSettings: () => Promise<void>;
}
