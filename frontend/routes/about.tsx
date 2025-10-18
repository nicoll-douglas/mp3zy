import PageHeading from "@/components/PageHeading";

export function meta() {
  return [{ title: `${import.meta.env.VITE_APP_NAME} | ABout` }];
}

export default function About() {
  return (
    <>
      <PageHeading>About</PageHeading>
    </>
  );
}
