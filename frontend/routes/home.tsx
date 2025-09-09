import { Button, Heading, Stack, Text } from "@chakra-ui/react";
import type { Route } from "./+types/home";

export function meta({}: Route.MetaArgs) {
  return [{ title: import.meta.env.VITE_APP_NAME }];
}

export default function Home() {
  async function pingPython() {
    try {
      const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/ping`);
      const json = await res.json();
      console.log(json);
    } catch (err) {
      console.error("Backend not reachable:", err);
    }
  }

  return (
    <main>
      <Stack gap={"4"}>
        <Heading size={"2xl"}>Home</Heading>
      </Stack>
    </main>
  );
}
