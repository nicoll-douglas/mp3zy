import { Field, Card, Heading, Stack, Button, Text } from "@chakra-ui/react";

export default function Settings() {
  return (
    <main>
      <Stack gap={"4"}>
        <Heading as={"h1"} size={"2xl"}>
          Settings
        </Heading>
        <Card.Root size={"sm"}>
          <Card.Header>
            <Heading as={"h2"} size={"lg"}>
              Downloads
            </Heading>
          </Card.Header>
          <Card.Body>
            <Field.Root>
              <Field.Label>Save Directory</Field.Label>
              <Field.HelperText>
                The directory on disk where music files downloaded and created
                are saved.
              </Field.HelperText>
              <Text></Text>
              <Button variant={"outline"} size={"sm"}>
                Browse
              </Button>

              <Field.ErrorText></Field.ErrorText>
            </Field.Root>
          </Card.Body>
        </Card.Root>
      </Stack>
    </main>
  );
}
