import { defaultConfig, createSystem, defineConfig } from "@chakra-ui/react";

const config = defineConfig({
  globalCss: {
    html: {
      colorPalette: "blue",
    },
  },
  theme: {
    tokens: {
      fonts: {
        body: {
          value: "Orbitron, sans-serif",
        },
        heading: {
          value: "Orbitron, sans-serif",
        },
      },
    },
  },
});

export const system = createSystem(defaultConfig, config);
