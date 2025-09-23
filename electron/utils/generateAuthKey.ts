import crypto from "crypto";

/**
 * Generate an authentication key for the backend to authenticate HTTP requests.
 *
 * @returns The authentication key.
 */
export default function generateAuthKey() {
  return crypto.randomBytes(16).toString("hex");
}
