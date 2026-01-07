import pluginVue from 'eslint-plugin-vue'
import tseslint from 'typescript-eslint'

export default [
  // Ignore patterns
  {
    ignores: ['dist/**', 'node_modules/**', '*.config.js', '*.config.ts'],
  },
  // Base TypeScript config
  ...tseslint.configs.recommended,
  // Vue config
  ...pluginVue.configs['flat/recommended'],
  // Custom rules
  {
    files: ['**/*.vue', '**/*.ts'],
    languageOptions: {
      parserOptions: {
        parser: tseslint.parser,
      },
    },
    rules: {
      // Vue specific
      'vue/multi-word-component-names': 'off',
      'vue/require-default-prop': 'off',
      'vue/no-v-html': 'warn',

      // TypeScript specific
      '@typescript-eslint/no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/no-explicit-any': 'warn',
      '@typescript-eslint/explicit-function-return-type': 'off',

      // General
      'no-console': ['warn', { allow: ['warn', 'error'] }],
    },
  },
]
