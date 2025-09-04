import { Flex, Icon as ChIcon, Link as ChLink } from "@chakra-ui/react";
import type React from "react";
import type { IconType } from "react-icons";
import { Link } from "react-router";

export default function HeaderLink({
  href,
  children,
  Icon,
}: {
  href: string;
  children: React.ReactNode;
  Icon: IconType;
}) {
  return (
    <ChLink asChild>
      <Link to={href} prefetch="intent">
        <Flex align={"center"} gap={"1.5"}>
          <ChIcon size={"inherit"} color={"blue.fg"}>
            <Icon />
          </ChIcon>
          {children}
        </Flex>
      </Link>
    </ChLink>
  );
}
