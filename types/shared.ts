export interface UserSettings {
  savePath: string;
}

export interface ElectronAPI {
  getSettings: () => Promise<UserSettings>;
}
