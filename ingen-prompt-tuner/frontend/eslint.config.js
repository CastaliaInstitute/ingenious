import pluginVue from 'eslint-plugin-vue'
import tseslint from 'typescript-eslint'
import jsdoc from 'eslint-plugin-jsdoc'
import security from 'eslint-plugin-security'

export default [
  // Ignore patterns
  {
    ignores: ['dist/**', 'node_modules/**', '*.config.js', '*.config.ts'],
  },
  // Base TypeScript config
  ...tseslint.configs.recommended,
  // Vue config
  ...pluginVue.configs['flat/recommended'],
  // JSDoc config for TypeScript
  jsdoc.configs['flat/recommended-typescript'],
  // Security config
  security.configs.recommended,
  // Custom rules
  {
    files: ['**/*.vue', '**/*.ts'],
    languageOptions: {
      parserOptions: {
        parser: tseslint.parser,
      },
    },
    plugins: {
      jsdoc,
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

      // Complexity rules
      'complexity': ['warn', { max: 10 }],
      'max-depth': ['warn', 4],
      'max-nested-callbacks': ['warn', 3],

      // General
      'no-console': ['warn', { allow: ['warn', 'error'] }],

      // JSDoc rules
      'jsdoc/require-jsdoc': ['warn', {
        require: {
          FunctionDeclaration: true,
          MethodDefinition: true,
          ClassDeclaration: true,
          ArrowFunctionExpression: false,
          FunctionExpression: false,
        },
        contexts: [
          'ExportNamedDeclaration > FunctionDeclaration',
          'ExportDefaultDeclaration > FunctionDeclaration',
        ],
      }],
      'jsdoc/require-description': 'warn',
      'jsdoc/require-param-description': 'warn',
      'jsdoc/require-returns-description': 'warn',
    },
  },
]
