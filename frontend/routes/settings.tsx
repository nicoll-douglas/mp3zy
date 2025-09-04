import {
  Field,
  Card,
  Heading,
  Stack,
  Input,
  Box,
  HStack,
  Button,
} from "@chakra-ui/react";

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
            <Box as={"form"} maxW={"xl"}>
              <Field.Root>
                <Field.Label>
                  Save Directory
                  <Field.RequiredIndicator />
                </Field.Label>
                <HStack w={"full"}>
                  <Input />
                  <Button>Browse</Button>
                </HStack>
                <Field.HelperText>
                  The directory on disk where music files downloaded and created
                  are saved.
                </Field.HelperText>
                <Field.ErrorText></Field.ErrorText>
              </Field.Root>
            </Box>
          </Card.Body>
        </Card.Root>
      </Stack>
    </main>
  );
}
