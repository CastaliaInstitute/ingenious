<script setup lang="ts">
  import { onMounted } from 'vue'
  import { useRevisionsStore } from '@/stores/revisions'
  import { useEditorStore } from '@/stores/editor'
  import Button from '@/components/common/Button.vue'
  import PromptCard from './PromptCard.vue'
  import EditorPanel from './EditorPanel.vue'

  const revisionsStore = useRevisionsStore()
  const editorStore = useEditorStore()

  onMounted(async () => {
    await revisionsStore.fetchRevisions()
    if (revisionsStore.activeRevision) {
      await revisionsStore.fetchPrompts()
    }
  })

  function handleRevisionChange(event: Event) {
    const target = event.target as HTMLSelectElement
    revisionsStore.setActiveRevision(target.value)
    editorStore.clearSelection()
  }

  function handleCreateRevision() {
    const name = prompt('Enter a name for the new revision:')
    if (name) {
      revisionsStore.createRevision(name)
    }
  }
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-8">
      <div>
        <label class="block text-sm font-medium text-taupe mb-2">Revision</label>
        <select
          :value="revisionsStore.activeRevision"
          class="w-64 px-3 py-2 bg-white border border-gray-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-shiraz/20 focus:border-shiraz"
          @change="handleRevisionChange"
        >
          <option
            v-for="revision in revisionsStore.revisions"
            :key="revision.id"
            :value="revision.id"
          >
            {{ revision.name }}
          </option>
        </select>
      </div>
      <Button @click="handleCreateRevision"> Create New Revision </Button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <PromptCard
        v-for="prompt in revisionsStore.prompts"
        :key="prompt.filename"
        :prompt="prompt"
        :selected="editorStore.selectedPrompt?.filename === prompt.filename"
        @click="editorStore.selectPrompt(prompt)"
      />
    </div>

    <EditorPanel v-if="editorStore.selectedPrompt" class="mt-8" />
  </div>
</template>
