import * as Ch from "@chakra-ui/react";
import type React from "react";

export default function SettingsGroup({
  children,
  heading,
}: {
  heading: string;
  children: React.ReactNode;
}) {
  return (
    <Ch.Card.Root size={"sm"}>
      <Ch.Card.Header>
        <Ch.Heading as={"h2"} size={"lg"}>
          {heading}
        </Ch.Heading>
      </Ch.Card.Header>
      <Ch.Card.Body>
        <Ch.Stack maxW={"lg"} gap="5">
          {children}
        </Ch.Stack>
      </Ch.Card.Body>
    </Ch.Card.Root>
  );
}
