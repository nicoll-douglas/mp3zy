import { Flex, HStack, Link as ChLink } from "@chakra-ui/react";
import { Link } from "react-router";
import HeaderLink from "./HeaderLink";
import { LuDownload, LuList, LuSettings } from "react-icons/lu";
import { FaSpotify } from "react-icons/fa";
import { ColorModeButton } from "../chakra/color-mode";

export default function Header() {
  return (
    <Flex
      py={"4"}
      justify={"space-between"}
      align={"center"}
      position={"sticky"}
      top={"0"}
    >
      <ChLink asChild fontWeight={"bold"} fontSize={"large"}>
        <Link to={"/"}>{import.meta.env.VITE_APP_NAME}</Link>
      </ChLink>
      <HStack gap={"6"}>
        <HeaderLink Icon={LuList} href="/downloads">
          Downloads
        </HeaderLink>
        <HeaderLink Icon={LuDownload} href="/new-download">
          New Download
        </HeaderLink>
        <HeaderLink Icon={FaSpotify} href="/spotify-sync">
          Download from Spotify
        </HeaderLink>
        <HeaderLink Icon={LuSettings} href="/settings">
          Settings
        </HeaderLink>
        <ColorModeButton size={"xs"} />
      </HStack>
    </Flex>
  );
}
