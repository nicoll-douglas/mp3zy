import * as Ch from "@chakra-ui/react";

export default function PageHeading({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <Ch.Heading as={"h1"} size={"2xl"}>
      {children}
    </Ch.Heading>
  );
}
