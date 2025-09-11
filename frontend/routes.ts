import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("./routes/home.tsx"),
  route("/settings", "./routes/settings.tsx"),
  route("/download", "./routes/download.tsx"),
] satisfies RouteConfig;
