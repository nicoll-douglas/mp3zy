import type { Route } from "./+types/spotify-sync";

export function meta({}: Route.MetaArgs) {
  return [{ title: "Sync from Spotify" }];
}

export default function SpotifySync() {
  return <main className="">hello</main>;
}
