import * as Ch from "@chakra-ui/react";
import SearchDownloadsForm from "./SearchDownloadsForm";
import SearchResults from "./SearchDownloadsResults";
import { SearchDownloadsFormProvider } from "../../../context/SearchDownloadsFormContext";
import UrlField from "./UrlField";

/**
 * Represents a stack of cards that together lay out the step for obtaining a source URL to submit and download from.
 */
export default function EnterUrlStep() {
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
