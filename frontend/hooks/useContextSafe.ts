import { useContext, type Context } from "react";

/**
 * Hook to safely consume a nullable react context.
 *
 * @param context The context to be consumed
 * @returns The non-null context value.
 */
export default function useSafeContext<T>(context: Context<T | null>): T {
  const contextValue = useContext(context);

  if (contextValue === null) {
    throw new Error("useSafeContext must be used inside its Provider");
  }

  return contextValue;
}
