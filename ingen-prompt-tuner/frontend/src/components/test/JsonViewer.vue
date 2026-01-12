<script setup lang="ts">
  import { computed, ref } from 'vue'

  const props = defineProps<{
    content: string
    maxHeight?: string
  }>()

  const copied = ref(false)
  const collapsedPaths = ref<Set<string>>(new Set())

  interface ParsedJson {
    valid: boolean
    data: unknown
  }

  const INVALID_JSON: ParsedJson = { valid: false, data: null }

  /**
   * Try to parse JSON string, returns null on failure
   */
  function tryParseJson(text: string): unknown | null {
    try {
      return JSON.parse(text)
    } catch {
      return null
    }
  }

  /**
   * Unwrap double-stringified JSON if applicable
   */
  function unwrapDoubleStringified(data: unknown): unknown {
    if (typeof data !== 'string') {
      return data
    }
    const innerData = tryParseJson(data)
    if (typeof innerData === 'object' && innerData !== null) {
      return innerData
    }
    return data
  }

  /**
   * Attempt direct JSON parse with double-stringify handling
   */
  function tryDirectParse(content: string): ParsedJson | null {
    const data = tryParseJson(content)
    if (data === null) {
      return null
    }
    return { valid: true, data: unwrapDoubleStringified(data) }
  }

  /**
   * Attempt to extract and parse JSON from within text
   */
  function tryExtractFromText(content: string): ParsedJson | null {
    const jsonStartIndex = findJsonStart(content)
    if (jsonStartIndex < 0) {
      return null
    }

    const potentialJson = content.substring(jsonStartIndex)

    // Try parsing from start index
    const directResult = tryParseJson(potentialJson)
    if (directResult !== null) {
      return { valid: true, data: directResult }
    }

    // Try to find matching bracket and parse
    const extracted = extractJsonSubstring(potentialJson)
    if (!extracted) {
      return null
    }

    const extractedResult = tryParseJson(extracted)
    if (extractedResult !== null) {
      return { valid: true, data: extractedResult }
    }

    return null
  }

  const parsedContent = computed<ParsedJson>(() => {
    const content = props.content?.trim() || ''
    if (!content) {
      return INVALID_JSON
    }

    return tryDirectParse(content) ?? tryExtractFromText(content) ?? INVALID_JSON
  })

  function findJsonStart(text: string): number {
    const objectStart = text.indexOf('{')
    const arrayStart = text.indexOf('[')
    if (objectStart === -1) return arrayStart
    if (arrayStart === -1) return objectStart
    return Math.min(objectStart, arrayStart)
  }

  interface ParserState {
    depth: number
    inString: boolean
    escapeNext: boolean
  }

  /**
   * Process a single character and update parser state
   * Returns the ending index if bracket matching is complete, -1 otherwise
   */
  function processCharacter(
    char: string,
    index: number,
    startChar: string,
    endChar: string,
    state: ParserState
  ): number {
    if (state.escapeNext) {
      state.escapeNext = false
      return -1
    }

    if (char === '\\' && state.inString) {
      state.escapeNext = true
      return -1
    }

    if (char === '"') {
      state.inString = !state.inString
      return -1
    }

    if (state.inString) {
      return -1
    }

    if (char === startChar) {
      state.depth++
    } else if (char === endChar) {
      state.depth--
      if (state.depth === 0) {
        return index
      }
    }

    return -1
  }

  function extractJsonSubstring(text: string): string | null {
    const startChar = text[0]
    const endChar = startChar === '{' ? '}' : ']'
    const state: ParserState = { depth: 0, inString: false, escapeNext: false }

    for (let i = 0; i < text.length; i++) {
      const endIndex = processCharacter(text[i], i, startChar, endChar, state)
      if (endIndex >= 0) {
        return text.substring(0, endIndex + 1)
      }
    }

    return null
  }

  function toggleCollapse(path: string) {
    if (collapsedPaths.value.has(path)) {
      collapsedPaths.value.delete(path)
    } else {
      collapsedPaths.value.add(path)
    }
    // Trigger reactivity
    collapsedPaths.value = new Set(collapsedPaths.value)
  }

  async function copyToClipboard() {
    try {
      await navigator.clipboard.writeText(props.content)
      copied.value = true
      setTimeout(() => {
        copied.value = false
      }, 2000)
    } catch {
      // Fallback
    }
  }

  const isTruncated = computed(() => {
    const content = props.content?.trim() || ''
    return content.endsWith('...')
  })
</script>

<template>
  <div class="relative">
    <button
      class="absolute top-2 right-2 p-1.5 rounded bg-white/80 hover:bg-white border border-gray-200 text-xs text-taupe transition-colors z-10"
      title="Copy to clipboard"
      @click="copyToClipboard"
    >
      <template v-if="copied"> Copied </template>
      <template v-else>
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
          />
        </svg>
      </template>
    </button>

    <div
      class="bg-desert rounded p-3 pr-12 text-xs font-mono overflow-auto"
      :style="{ maxHeight: maxHeight || '400px' }"
    >
      <template v-if="parsedContent.valid">
        <JsonNode
          :data="parsedContent.data"
          :path="'root'"
          :collapsed-paths="collapsedPaths"
          @toggle="toggleCollapse"
        />
      </template>
      <template v-else>
        <div v-if="isTruncated" class="mb-2 text-amber-600 text-xs italic">
          Content truncated - JSON formatting unavailable
        </div>
        <pre class="whitespace-pre-wrap text-mine">{{ content }}</pre>
      </template>
    </div>
  </div>
</template>

<script lang="ts">
  import { defineComponent, h, type PropType, type VNode } from 'vue'

  type JsonNodeComponent = ReturnType<typeof defineComponent>

  const JsonNode: JsonNodeComponent = defineComponent({
    name: 'JsonNode',
    props: {
      data: {
        type: null as unknown as PropType<unknown>,
        required: true,
      },
      path: {
        type: String,
        required: true,
      },
      collapsedPaths: {
        type: Object as PropType<Set<string>>,
        required: true,
      },
      indent: {
        type: Number,
        default: 0,
      },
      isLast: {
        type: Boolean,
        default: true,
      },
    },
    emits: ['toggle'],
    setup(props, { emit }): () => VNode {
      const getType = (value: unknown): string => {
        if (value === null) return 'null'
        if (Array.isArray(value)) return 'array'
        return typeof value
      }

      const isCollapsible = (value: unknown): boolean => {
        return (typeof value === 'object' && value !== null) || Array.isArray(value)
      }

      const isCollapsed = (): boolean => {
        return props.collapsedPaths.has(props.path)
      }

      const toggle = (): void => {
        emit('toggle', props.path)
      }

      const getPreview = (value: unknown): string => {
        if (Array.isArray(value)) {
          return `[${value.length} items]`
        }
        if (typeof value === 'object' && value !== null) {
          const keys = Object.keys(value)
          return `{${keys.length} keys}`
        }
        return ''
      }

      const renderValue = (value: unknown): (string | VNode)[] => {
        const type = getType(value)

        if (type === 'null') {
          return [h('span', { class: 'text-gray-500' }, 'null')]
        }
        if (type === 'boolean') {
          return [h('span', { class: 'text-purple-600' }, String(value))]
        }
        if (type === 'number') {
          return [h('span', { class: 'text-blue-600' }, String(value))]
        }
        if (type === 'string') {
          const strValue = value as string
          // Truncate long strings for display
          const displayValue = strValue.length > 200 ? strValue.substring(0, 200) + '...' : strValue
          return [h('span', { class: 'text-green-700' }, `"${displayValue}"`)]
        }

        return [h('span', { class: 'text-mine' }, String(value))]
      }

      return (): VNode => {
        const indentStyle = { paddingLeft: `${props.indent * 16}px` }
        const comma = props.isLast ? '' : ','

        if (!isCollapsible(props.data)) {
          return h('div', { style: indentStyle }, [...renderValue(props.data), comma])
        }

        const collapsed = isCollapsed()
        const isArray = Array.isArray(props.data)
        const openBracket = isArray ? '[' : '{'
        const closeBracket = isArray ? ']' : '}'

        if (collapsed) {
          return h('div', { style: indentStyle }, [
            h(
              'button',
              {
                class: 'text-taupe hover:text-shiraz mr-1 focus:outline-none',
                onClick: toggle,
              },
              '+'
            ),
            h('span', { class: 'text-mine' }, openBracket),
            h('span', { class: 'text-gray-500 italic' }, ` ${getPreview(props.data)} `),
            h('span', { class: 'text-mine' }, closeBracket + comma),
          ])
        }

        const entries: Array<{ key: string | number; value: unknown }> = isArray
          ? (props.data as unknown[]).map((v, i) => ({ key: i, value: v }))
          : Object.entries(props.data as Record<string, unknown>).map(([k, v]) => ({
              key: k,
              value: v,
            }))

        const children: VNode[] = entries.map((entry, index): VNode => {
          const childPath = `${props.path}.${entry.key}`
          const isLastChild = index === entries.length - 1
          const childIndent = props.indent + 1

          if (isArray) {
            return h(JsonNode, {
              data: entry.value,
              path: childPath,
              collapsedPaths: props.collapsedPaths,
              indent: childIndent,
              isLast: isLastChild,
              onToggle: (p: string) => emit('toggle', p),
            })
          }

          // Object key-value pair
          const keySpan = h('span', { class: 'text-shiraz' }, `"${entry.key}"`)
          const colonSpan = h('span', { class: 'text-mine' }, ': ')

          if (isCollapsible(entry.value)) {
            return h('div', { key: entry.key }, [
              h('div', { style: { paddingLeft: `${childIndent * 16}px` } }, [keySpan, colonSpan]),
              h(JsonNode, {
                data: entry.value,
                path: childPath,
                collapsedPaths: props.collapsedPaths,
                indent: childIndent,
                isLast: isLastChild,
                onToggle: (p: string) => emit('toggle', p),
              }),
            ])
          }

          return h('div', { key: entry.key, style: { paddingLeft: `${childIndent * 16}px` } }, [
            keySpan,
            colonSpan,
            ...renderValue(entry.value),
            isLastChild ? '' : ',',
          ])
        })

        return h('div', { style: indentStyle }, [
          h(
            'button',
            {
              class: 'text-taupe hover:text-shiraz mr-1 focus:outline-none',
              onClick: toggle,
            },
            '-'
          ),
          h('span', { class: 'text-mine' }, openBracket),
          ...children,
          h('div', { style: { paddingLeft: `${props.indent * 16}px` } }, closeBracket + comma),
        ])
      }
    },
  })
</script>
