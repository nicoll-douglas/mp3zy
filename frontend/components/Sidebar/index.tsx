import * as Ch from "@chakra-ui/react";
import { LuList, LuDownload, LuSettings } from "react-icons/lu";
import SidebarButtonLink from "./SidebarButtonLink";
import { FaSpotify } from "react-icons/fa";
import { Link } from "react-router";
import Logo from "../Logo";
import { ColorModeButton } from "../chakra-ui/color-mode";

export default function Sidebar() {
  return (
    <Ch.Stack
      gap={"4"}
      minWidth={"2xs"}
      position={"sticky"}
      top={"4"}
      height={"calc(100dvh - 32px)"}
    >
      <Ch.Card.Root size={"sm"}>
        <Ch.Card.Body>
          <Ch.HStack width={"full"}>
            <Ch.Link asChild fontWeight={"bold"}>
              <Link to={"/"}>
                <Logo />
                {import.meta.env.VITE_APP_NAME}
              </Link>
            </Ch.Link>
            <Ch.Spacer />
            <ColorModeButton size={"xs"} />
          </Ch.HStack>
        </Ch.Card.Body>
      </Ch.Card.Root>
      <Ch.Card.Root size={"sm"} flex={"1"}>
        <Ch.Card.Body overflowY={"auto"}>
          <Ch.VStack width={"full"}>
            <SidebarButtonLink href="/downloads" Icon={LuList}>
              Downloads
            </SidebarButtonLink>
            <SidebarButtonLink Icon={LuDownload} href="/download">
              New Download
            </SidebarButtonLink>
            <SidebarButtonLink Icon={FaSpotify} href="/spotify-sync">
              Download from Spotify
            </SidebarButtonLink>
            <SidebarButtonLink Icon={LuSettings} href="/settings">
              Settings
            </SidebarButtonLink>
          </Ch.VStack>
        </Ch.Card.Body>
      </Ch.Card.Root>
    </Ch.Stack>
  );
}
