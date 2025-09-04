import {
  Field,
  Card,
  Heading,
  Stack,
  Button,
  Text,
  Group,
  Input,
} from "@chakra-ui/react";
import useSettings from "@/hooks/useSettings";
import { LuFolder } from "react-icons/lu";

export default function Settings() {
  const { getSettingsQuery, updateSavePathMutation, restoreSettingsMutation } =
    useSettings();

  let savePath = "";
  if (getSettingsQuery.data) {
    savePath = getSettingsQuery.data.savePath;
  } else if (getSettingsQuery.isLoading) {
    savePath = "Loading...";
  } else if (getSettingsQuery.error) {
    savePath = getSettingsQuery.error.message;
  }

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
            <Field.Root maxW={"lg"}>
              <Field.Label>Save Directory</Field.Label>
              <Group attached w="full">
                <Input
                  value={savePath}
                  disabled
                  cursor={"default"}
                  title={savePath}
                  textOverflow={"ellipsis"}
                />
                <Button
                  variant={"outline"}
                  onClick={() => updateSavePathMutation.mutate()}
                  disabled={updateSavePathMutation.isPending}
                >
                  <LuFolder /> Change
                </Button>
              </Group>
              <Field.HelperText>
                The directory on disk where music files downloaded and created
                are saved.
              </Field.HelperText>
            </Field.Root>
          </Card.Body>
        </Card.Root>
        <Card.Root>
          <Card.Header>
            <Heading as="h2" size={"lg"}>
              General
            </Heading>
          </Card.Header>
          <Card.Body>
            <Field.Root>
              <Field.Label>Restore Defaults</Field.Label>
              <Field.HelperText>Restore the default settings.</Field.HelperText>
              <Button
                size={"xs"}
                colorPalette={"red"}
                onClick={() => restoreSettingsMutation.mutate()}
              >
                Restore
              </Button>
            </Field.Root>
          </Card.Body>
        </Card.Root>
      </Stack>
    </main>
  );
}
