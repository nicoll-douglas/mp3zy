import * as Ch from "@chakra-ui/react";
import type { ReactNode } from "react";

export interface SettingsGroupProps {
  /**
   * The heading of the settings group to go in the card header.
   */
  heading: string;

  /**
   * The settings management components to go in the body of the card.
   */
  children: ReactNode;
}

/**
 * Represents a card container for a group of related settings.
 */
export default function SettingsGroup({
  children,
  heading,
}: SettingsGroupProps) {
  return (
    <Ch.Card.Root size={"sm"}>
      <Ch.Card.Header>
        <Ch.Card.Title>{heading}</Ch.Card.Title>
      </Ch.Card.Header>
      <Ch.Card.Body>
        <Ch.Stack maxW={"lg"} gap="5">
          {children}
        </Ch.Stack>
      </Ch.Card.Body>
    </Ch.Card.Root>
  );
}
