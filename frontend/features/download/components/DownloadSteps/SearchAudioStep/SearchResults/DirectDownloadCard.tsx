import { Card, Button, Stack, Text } from "@chakra-ui/react";
import { LuChevronRight } from "react-icons/lu";

export default function DirectDownloadCard() {
  return (
    <Card.Root size={"sm"}>
      <Card.Body>
        <Stack alignItems={"start"}>
          <Text>
            Can't find the video you're looking for? Try downloading with a link
            directly (Coming soon).
          </Text>
          <Button size={"xs"} disabled>
            Go
            <LuChevronRight />
          </Button>
        </Stack>
      </Card.Body>
    </Card.Root>
  );
}
