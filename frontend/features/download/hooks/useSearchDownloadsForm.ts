import { useState, type BaseSyntheticEvent } from "react";
import { useForm, type UseFormReturn } from "react-hook-form";
import {
  type GetDownloadsSearchRequest,
  type GetDownloadsSearchResponse,
} from "../types";
import searchDownloads from "../services/searchDownloads";

/**
 * Return type for the useSearchDownloadsForm hook.
 */
export interface UseSearchDownloadsFormReturn {
  /**
   * The response to the form submission request if submitted.
   */
  response: GetDownloadsSearchResponse | null;

  /**
   * The form.
   */
  form: UseFormReturn<
    GetDownloadsSearchRequest,
    any,
    GetDownloadsSearchRequest
  >;

  /**
   * The form submission handler.
   */
  onFormSubmit: (
    e?: BaseSyntheticEvent<object, any, any> | undefined
  ) => Promise<void>;
}

/**
 * Hook to provide a form that uses the search downloads service on submission.
 *
 * @returns The form, the request response if submitted, and the form submission handler.
 */
export default function useSearchDownloadsForm(): UseSearchDownloadsFormReturn {
  const form = useForm<GetDownloadsSearchRequest>();
  const [response, setResponse] = useState<GetDownloadsSearchResponse | null>(
    null
  );

  const onFormSubmit = form.handleSubmit(async (data) => {
    const res = await searchDownloads(data);
    setResponse(res);
  });

  return {
    response,
    form,
    onFormSubmit,
  };
}
