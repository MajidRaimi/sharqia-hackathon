import tseslint from "typescript-eslint";

export const reactInternalConfig = [
  ...tseslint.configs.recommended,
  {
    rules: {
      "no-redeclare": "off",
    },
  },
];
