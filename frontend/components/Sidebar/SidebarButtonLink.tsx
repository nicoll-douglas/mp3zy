import * as Ch from "@chakra-ui/react";
import { Link } from "react-router";
import { type IconType } from "react-icons";

export interface SidebarButtonLinkProps {
  href: string;
  children: React.ReactNode;
  Icon: IconType;
}

export default function SidebarButtonLink({
  href,
  children,
  Icon,
}: SidebarButtonLinkProps) {
  return (
    <Ch.Button
      justifyContent={"start"}
      variant={"ghost"}
      width={"full"}
      asChild
    >
      <Ch.Link textDecoration={"none"} asChild>
        <Link to={href} prefetch="intent">
          <Ch.Flex gap={"2"}>
            <Ch.Icon size={"inherit"} color={"blue.fg"}>
              <Icon />
            </Ch.Icon>
            {children}
          </Ch.Flex>
        </Link>
      </Ch.Link>
    </Ch.Button>
  );
}
