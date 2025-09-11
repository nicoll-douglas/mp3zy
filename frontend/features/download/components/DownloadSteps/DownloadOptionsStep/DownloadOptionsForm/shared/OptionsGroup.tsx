import * as Ch from "@chakra-ui/react";
import type React from "react";

export default function OptionsGroup({
  heading,
  children,
}: {
  heading: string;
  children: React.ReactNode;
}) {
  return (
    <Ch.Box>
      <Ch.Heading as={"h3"} size={"md"} mb={"4"}>
        {heading}
      </Ch.Heading>
      <Ch.Stack maxW={"lg"} gap="5">
        {children}
      </Ch.Stack>
    </Ch.Box>
  );
}
