export interface UserSettings {
  default_download_dir: string;
}

export interface ElectronAPI {
  getSettings: () => Promise<UserSettings | null>;

  updateSettings: (updatedSettings: Partial<UserSettings>) => Promise<boolean>;

  pickDirectory: (dialogTitle: string) => Promise<string | null>;

  restoreSettings: () => Promise<boolean>;
}
