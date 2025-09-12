import * as Ch from "@chakra-ui/react";
import { Link } from "react-router";
import { LuCircleCheck } from "react-icons/lu";
import { useDownloadOptionsFormContext } from "../../context/DownloadOptionsFormContext";
import type { ReactNode } from "react";
import { MdOutlineQueue } from "react-icons/md";
import { IoWarningOutline } from "react-icons/io5";

export default function CompletedContent() {
  const { downloadStatus } = useDownloadOptionsFormContext();

  let title: ReactNode = "";
  let text: ReactNode = "";
  let icon: ReactNode = "";

  const DownloadsLink = () => (
    <Ch.Link asChild>
      <Link to={"/downloads"}>downloads</Link>
    </Ch.Link>
  );

  switch (downloadStatus) {
    case "downloading":
      title = "Download Started";
      text = (
        <>
          Your download has started, check the <DownloadsLink /> screen for
          progress.
        </>
      );
      icon = <LuCircleCheck />;
      break;
    case "queued":
      title = "Download Queued";
      text = (
        <>
          Your download has been queued, check the <DownloadsLink /> screen for
          updates.
        </>
      );
      icon = <MdOutlineQueue />;
      break;
    default:
      title = "Failed to Start Download";
      text = "The app failed to start your download, please try again later.";
      icon = <IoWarningOutline />;
  }

  return (
    <Ch.Steps.CompletedContent>
      <Ch.Card.Root size={"sm"}>
        <Ch.Card.Header>
          <Ch.HStack>
            <Ch.Icon size={"lg"}>{icon}</Ch.Icon>
            <Ch.Card.Title>{title}</Ch.Card.Title>
          </Ch.HStack>
        </Ch.Card.Header>
        <Ch.Card.Body>
          <Ch.Text>{text}</Ch.Text>
        </Ch.Card.Body>
      </Ch.Card.Root>
    </Ch.Steps.CompletedContent>
  );
}
