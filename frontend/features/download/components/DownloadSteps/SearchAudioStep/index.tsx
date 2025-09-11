import * as Ch from "@chakra-ui/react";
import SearchForm from "./SearchForm";
import SearchResults from "./SearchResults";

export default function SearchAudioStep() {
  return (
    <Ch.Steps.Content index={0}>
      <Ch.Stack gap={"4"}>
        <SearchForm />
        <SearchResults />
      </Ch.Stack>
    </Ch.Steps.Content>
  );
}
