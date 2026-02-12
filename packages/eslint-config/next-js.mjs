import pluginNext from "@next/eslint-plugin-next";
import tseslint from "typescript-eslint";

export const nextJsConfig = [
  ...tseslint.configs.recommended,
  {
    plugins: {
      "@next/next": pluginNext,
    },
    rules: {
      ...pluginNext.configs.recommended.rules,
      ...pluginNext.configs["core-web-vitals"].rules,
    },
  },
];
