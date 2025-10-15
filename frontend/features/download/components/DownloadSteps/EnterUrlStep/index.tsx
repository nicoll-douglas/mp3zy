import * as Ch from "@chakra-ui/react";
import SearchDownloadsForm from "./SearchDownloadsForm";
import SearchResults from "./SearchDownloadsResults";
import { SearchDownloadsFormProvider } from "../../../context/SearchDownloadsFormContext";
import UrlField from "./UrlField";

export default function SearchDownloadsStep() {
  return (
    <SearchDownloadsFormProvider>
      <Ch.Stack gap={"4"}>
        <UrlField />
        <SearchDownloadsForm />
        <SearchResults />
      </Ch.Stack>
    </SearchDownloadsFormProvider>
  );
}
