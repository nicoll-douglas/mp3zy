import crypto from "crypto";

export default function generateAuthKey() {
  return crypto.randomBytes(16).toString("hex");
}
