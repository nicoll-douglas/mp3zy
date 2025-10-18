import * as Ch from "@chakra-ui/react";
import { LuSettings } from "react-icons/lu";
import { Link } from "react-router";
import type { IconButtonProps } from "@chakra-ui/react";

export default function SettingsButton(props: IconButtonProps) {
  return (
    <Ch.IconButton asChild variant={"ghost"} {...props}>
      <Ch.Link asChild>
        <Link to={"/settings"}>
          <Ch.Icon size={"inherit"} color={"blue.fg"}>
            <LuSettings />
          </Ch.Icon>
        </Link>
      </Ch.Link>
    </Ch.IconButton>
  );
}
