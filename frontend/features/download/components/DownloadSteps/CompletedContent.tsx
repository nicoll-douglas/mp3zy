import * as Ch from "@chakra-ui/react";
import { Link } from "react-router";
import { LuCircleCheck } from "react-icons/lu";
import { useDownloadOptionsFormContext } from "../../context/DownloadOptionsFormContext";

export default function CompletedContent() {
  const { taskId } = useDownloadOptionsFormContext();

  return (
    <Ch.Steps.CompletedContent>
      <Ch.Card.Root size={"sm"}>
        <Ch.Card.Header>
          <Ch.HStack>
            <Ch.Icon size={"lg"}>
              <LuCircleCheck />
            </Ch.Icon>
            <Ch.Card.Title>Download Started</Ch.Card.Title>
          </Ch.HStack>
          <Ch.Card.Description>Task ID: {taskId}</Ch.Card.Description>
        </Ch.Card.Header>
        <Ch.Card.Body>
          <Ch.Text>
            Your download has started, check the{" "}
            <Ch.Link asChild>
              <Link to={"/downloads"}>downloads</Link>
            </Ch.Link>{" "}
            screen for progress.
          </Ch.Text>
        </Ch.Card.Body>
      </Ch.Card.Root>
    </Ch.Steps.CompletedContent>
  );
}
