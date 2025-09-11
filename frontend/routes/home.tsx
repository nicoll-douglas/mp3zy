import * as Ch from "@chakra-ui/react";
import type { Route } from "./+types/home";
import getBackendAuthHeaders from "@/services/getBackendAuthHeaders";

export function meta({}: Route.MetaArgs) {
  return [{ title: import.meta.env.VITE_APP_NAME }];
}

export default function Home() {
  const headers = getBackendAuthHeaders();

  async function pingPython() {
    try {
      const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/ping`, {
        headers,
      });
      const json = await res.json();
      console.log(json);
    } catch (err) {
      console.error("Backend not reachable:", err);
    }
  }

  return (
    <>
      <Ch.Heading size={"2xl"}>Home</Ch.Heading>
      <Ch.Button onClick={pingPython}>Ping Backend</Ch.Button>
    </>
  );
}
