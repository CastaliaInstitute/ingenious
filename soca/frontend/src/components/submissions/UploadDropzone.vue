<script setup lang="ts">
  /**
   * UploadDropzone component for file uploads via drag-and-drop or click.
   * Shows upload progress and accepts multiple document formats.
   */
  import { ref } from 'vue'

  defineProps<{
    progress: number | null
  }>()

  const emit = defineEmits<{
    'files-selected': [files: File[]]
  }>()

  const isDragging = ref(false)
  const fileInput = ref<HTMLInputElement>()

  const acceptedTypes = '.pdf,.txt,.md,.docx,.rtf'

  /**
   * Handles drag over events for the drop zone.
   * @param e - The drag event.
   */
  function handleDragOver(e: DragEvent) {
    e.preventDefault()
    isDragging.value = true
  }

  /**
   * Handles drag leave events for the drop zone.
   */
  function handleDragLeave() {
    isDragging.value = false
  }

  /**
   * Handles file drop events and emits the selected files.
   * @param e - The drop event.
   */
  function handleDrop(e: DragEvent) {
    e.preventDefault()
    isDragging.value = false

    if (e.dataTransfer?.files) {
      emit('files-selected', Array.from(e.dataTransfer.files))
    }
  }

  /**
   * Opens the file picker dialog when the zone is clicked.
   */
  function handleClick() {
    fileInput.value?.click()
  }

  /**
   * Handles file selection from the file input.
   * @param e - The change event from the file input.
   */
  function handleFileChange(e: Event) {
    const input = e.target as HTMLInputElement
    if (input.files?.length) {
      emit('files-selected', Array.from(input.files))
      input.value = ''
    }
  }
</script>

<template>
  <div
    :class="[
      'border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors',
      isDragging ? 'border-shiraz bg-shiraz/5' : 'border-gray-300 hover:border-shiraz/50',
    ]"
    @dragover="handleDragOver"
    @dragleave="handleDragLeave"
    @drop="handleDrop"
    @click="handleClick"
  >
    <input
      ref="fileInput"
      type="file"
      :accept="acceptedTypes"
      multiple
      class="hidden"
      @change="handleFileChange"
    />

    <template v-if="progress !== null">
      <div class="mb-2">
        <svg
          class="w-10 h-10 mx-auto text-shiraz animate-pulse"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
          />
        </svg>
      </div>
      <p class="text-sm font-medium text-mine mb-1">Uploading...</p>
      <div class="w-48 mx-auto bg-gray-200 rounded-full h-2">
        <div class="bg-shiraz h-2 rounded-full transition-all" :style="{ width: `${progress}%` }" />
      </div>
      <p class="text-xs text-taupe mt-2">{{ progress }}%</p>
    </template>

    <template v-else>
      <div class="mb-2">
        <svg
          class="w-10 h-10 mx-auto text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
          />
        </svg>
      </div>
      <p class="text-sm font-medium text-mine mb-1">Drop files here or click to upload</p>
      <p class="text-xs text-taupe">PDF, TXT, MD, DOCX, RTF supported</p>
    </template>
  </div>
</template>
