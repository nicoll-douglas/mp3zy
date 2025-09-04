import { Button } from "@chakra-ui/react";
import type { Route } from "./+types/home";

export function meta({}: Route.MetaArgs) {
  return [{ title: import.meta.env.VITE_APP_NAME }];
}

export default function Home() {
  async function pingPython() {
    try {
      const res = await fetch("http://127.0.0.1:8888/ping");
      const json = await res.json();
      console.log(json);
    } catch (err) {
      console.error("Backend not reachable:", err);
    }
  }

  return (
    <main>
      <Button onClick={pingPython} variant={"subtle"}>
        Ping Backend
      </Button>
    </main>
  );
}
