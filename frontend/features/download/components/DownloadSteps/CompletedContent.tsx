import * as Ch from "@chakra-ui/react";
import { Link } from "react-router";
import { LuCircleCheck } from "react-icons/lu";
import { useDownloadFormContext } from "../../context/DownloadFormContext";

/**
 * Represents a card that shows the completed content when all download steps are completed and the form submitted.
 */
export default function CompletedContent() {
  const { response } = useDownloadFormContext();

  return (
    <Ch.Card.Root size={"sm"}>
      <Ch.Card.Header>
        <Ch.HStack>
          <Ch.Icon size={"lg"}>
            <LuCircleCheck />
          </Ch.Icon>
          <Ch.Card.Title>Download Queued</Ch.Card.Title>
        </Ch.HStack>
      </Ch.Card.Header>

      <Ch.Card.Body>
        <Ch.Text>
          Your download has been queued and should start shortly, check the{" "}
          <Ch.Link asChild>
            <Link to={"/downloads"}>downloads</Link>
          </Ch.Link>{" "}
          screen for updates.
        </Ch.Text>
      </Ch.Card.Body>
    </Ch.Card.Root>
  );
}
