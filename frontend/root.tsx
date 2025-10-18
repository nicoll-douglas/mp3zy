import { Links, Meta, Outlet, Scripts, ScrollRestoration } from "react-router";

import type { Route } from "./+types/root";
import "./app.css";
import { Provider as ChProvider } from "@/components/chakra-ui/provider";
import * as Ch from "@chakra-ui/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import Sidebar from "@/components/Sidebar";

const queryClient = new QueryClient();

export const links: Route.LinksFunction = () => [
  { rel: "preconnect", href: "https://fonts.googleapis.com" },
  {
    rel: "preconnect",
    href: "https://fonts.gstatic.com",
    crossOrigin: "anonymous",
  },
  {
    rel: "stylesheet",
    href: "https://fonts.googleapis.com/css2?family=Orbitron:wght@400..900&display=swap",
  },
];

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <Meta />
        <Links />
      </head>
      <body>
        {children}
        <ScrollRestoration />
        <Scripts />
      </body>
    </html>
  );
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ChProvider>
        <Ch.Container
          py={"4"}
          px={"4"}
          minHeight={"100dvh"}
          display={"flex"}
          gap={"4"}
          alignItems={"start"}
        >
          <Sidebar />
          <Ch.Stack
            gap={"4"}
            pt={{ base: "8", lg: "10" }}
            mt={"2px"}
            flex={1}
            overflow={"auto"}
          >
            <Outlet />
          </Ch.Stack>
        </Ch.Container>
      </ChProvider>
    </QueryClientProvider>
  );
}
