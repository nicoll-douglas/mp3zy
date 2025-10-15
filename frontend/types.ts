/**
 * Represents the various possible codecs to use for a track download.
 */
export type TrackCodec = "mp3" | "flac";

/**
 * Represents the various possible bitrates to use for a track download.
 */
export type TrackBitrate = "320" | "192" | "128";

/**
 * Represents artist name metadata.
 */
export type TrackArtistNames = [string, ...string[]];
