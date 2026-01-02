<script setup lang="ts">
  import { useEditorStore } from '@/stores/editor'
  import { useRevisionsStore } from '@/stores/revisions'
  import { promptsService } from '@/services/prompts.service'
  import Button from '@/components/common/Button.vue'
  import CodeEditor from './CodeEditor.vue'

  const editorStore = useEditorStore()
  const revisionsStore = useRevisionsStore()

  async function handleSave() {
    if (editorStore.selectedPrompt && editorStore.modifiedContent) {
      await promptsService.update(
        revisionsStore.activeRevision,
        editorStore.selectedPrompt.filename,
        editorStore.modifiedContent
      )
    }
  }

  function handleEditorChange(value: string) {
    editorStore.updateContent(value)
  }
</script>

<template>
  <div
    v-if="editorStore.selectedPrompt"
    class="bg-white rounded-lg border border-gray-200 overflow-hidden"
  >
    <div class="flex items-center justify-between px-5 py-3 border-b border-gray-200">
      <div class="flex items-center gap-3">
        <span class="text-sm font-medium text-mine">{{ editorStore.selectedPrompt.filename }}</span>
        <span class="text-xs text-taupe">Last modified 2 hours ago</span>
      </div>
      <div class="flex items-center gap-2">
        <Button
          size="sm"
          variant="secondary"
          :disabled="!editorStore.hasChanges"
          @click="editorStore.discardChanges()"
        >
          Discard
        </Button>
        <Button size="sm" :disabled="!editorStore.hasChanges" @click="handleSave"> Save </Button>
      </div>
    </div>

    <div class="editor-wrapper">
      <CodeEditor
        :model-value="editorStore.modifiedContent || ''"
        @update:model-value="handleEditorChange"
      />
    </div>

    <div class="px-5 py-3 border-t border-gray-200 flex items-center gap-2 flex-wrap">
      <span class="text-xs text-taupe">Variables:</span>
      <span
        v-for="variable in editorStore.extractedVariables"
        :key="variable"
        class="px-2 py-0.5 text-xs rounded font-mono bg-yellow-100 text-yellow-800"
      >
        {{ variable }}
      </span>
      <span v-if="editorStore.extractedVariables.length === 0" class="text-xs text-taupe italic">
        No variables detected
      </span>
    </div>
  </div>
</template>
