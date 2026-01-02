<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useSubmissionsStore } from '@/stores/submissions'
import Card from '@/components/common/Card.vue'
import Spinner from '@/components/common/Spinner.vue'
import UploadDropzone from './UploadDropzone.vue'
import SubmissionItem from './SubmissionItem.vue'
import type { Submission } from '@/types'

const submissionsStore = useSubmissionsStore()
const isDragging = ref(false)
const selectedSubmission = ref<Submission | null>(null)
const isEditing = ref(false)
const editName = ref('')
const editDescription = ref('')

onMounted(() => {
  submissionsStore.fetchSubmissions()
})

async function handleFilesSelected(files: File[]) {
  for (const file of files) {
    await submissionsStore.uploadSubmission(file, file.name)
  }
}

function selectSubmission(submission: Submission) {
  if (selectedSubmission.value?.id === submission.id) {
    selectedSubmission.value = null
  } else {
    selectedSubmission.value = submission
    isEditing.value = false
  }
}

function startEdit() {
  if (selectedSubmission.value) {
    editName.value = selectedSubmission.value.name
    editDescription.value = selectedSubmission.value.description || ''
    isEditing.value = true
  }
}

function cancelEdit() {
  isEditing.value = false
}

async function saveEdit() {
  if (selectedSubmission.value && editName.value.trim()) {
    await submissionsStore.updateSubmission(selectedSubmission.value.id, {
      name: editName.value.trim(),
      description: editDescription.value.trim()
    })
    selectedSubmission.value = {
      ...selectedSubmission.value,
      name: editName.value.trim(),
      description: editDescription.value.trim()
    }
    isEditing.value = false
  }
}

function formatFileSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}
</script>

<template>
  <div>
    <div class="mb-8">
      <h1 class="text-xl font-semibold text-mine">Submissions</h1>
      <p class="text-sm text-taupe mt-1">Upload and manage documents for evaluation</p>
    </div>

    <UploadDropzone
      class="mb-8"
      @files-selected="handleFilesSelected"
      :progress="submissionsStore.uploadProgress"
    />

    <div v-if="submissionsStore.loading" class="flex justify-center py-8">
      <Spinner text="Loading submissions..." />
    </div>

    <div v-else-if="submissionsStore.error" class="text-center py-8 text-red-600">
      {{ submissionsStore.error }}
    </div>

    <div v-else class="space-y-3">
      <SubmissionItem
        v-for="submission in submissionsStore.submissions"
        :key="submission.id"
        :submission="submission"
        :selected="selectedSubmission?.id === submission.id"
        @click="selectSubmission(submission)"
        @delete="submissionsStore.deleteSubmission(submission.id)"
      />

      <div v-if="submissionsStore.submissions.length === 0" class="text-center py-8 text-taupe">
        No submissions yet. Upload your first document to get started.
      </div>
    </div>

    <!-- Details Panel -->
    <div v-if="selectedSubmission" class="mt-6 bg-white rounded-lg border border-gray-200 p-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-medium text-mine">Submission Details</h3>
        <div class="flex gap-2">
          <button
            v-if="!isEditing"
            @click="startEdit"
            class="px-3 py-1 text-sm bg-desert text-mine rounded hover:bg-opacity-80"
          >
            Edit
          </button>
          <button
            @click="selectedSubmission = null"
            class="px-3 py-1 text-sm text-taupe hover:text-mine"
          >
            Close
          </button>
        </div>
      </div>

      <!-- View Mode -->
      <div v-if="!isEditing" class="space-y-4">
        <div>
          <p class="text-xs text-taupe uppercase tracking-wide">Name</p>
          <p class="text-sm text-mine">{{ selectedSubmission.name }}</p>
        </div>
        <div>
          <p class="text-xs text-taupe uppercase tracking-wide">Description</p>
          <p class="text-sm text-mine">{{ selectedSubmission.description || 'No description' }}</p>
        </div>
        <div class="grid grid-cols-3 gap-4">
          <div>
            <p class="text-xs text-taupe uppercase tracking-wide">File Name</p>
            <p class="text-sm text-mine">{{ selectedSubmission.fileName }}</p>
          </div>
          <div>
            <p class="text-xs text-taupe uppercase tracking-wide">Size</p>
            <p class="text-sm text-mine">{{ formatFileSize(selectedSubmission.fileSize) }}</p>
          </div>
          <div>
            <p class="text-xs text-taupe uppercase tracking-wide">Uploaded</p>
            <p class="text-sm text-mine">{{ formatDate(selectedSubmission.uploadedAt) }}</p>
          </div>
        </div>
        <div v-if="selectedSubmission.extractedText">
          <p class="text-xs text-taupe uppercase tracking-wide mb-2">Content Preview</p>
          <p class="text-sm text-mine bg-desert p-3 rounded max-h-32 overflow-y-auto whitespace-pre-wrap">
            {{ selectedSubmission.extractedText.substring(0, 500) }}{{ selectedSubmission.extractedText.length > 500 ? '...' : '' }}
          </p>
        </div>
      </div>

      <!-- Edit Mode -->
      <div v-else class="space-y-4">
        <div>
          <label class="block text-xs text-taupe uppercase tracking-wide mb-1">Name</label>
          <input
            v-model="editName"
            type="text"
            class="w-full px-3 py-2 border border-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-shiraz"
            placeholder="Submission name"
          />
        </div>
        <div>
          <label class="block text-xs text-taupe uppercase tracking-wide mb-1">Description</label>
          <textarea
            v-model="editDescription"
            rows="3"
            class="w-full px-3 py-2 border border-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-shiraz"
            placeholder="Optional description"
          ></textarea>
        </div>
        <div class="flex gap-2 justify-end">
          <button
            @click="cancelEdit"
            class="px-4 py-2 text-sm text-taupe hover:text-mine"
          >
            Cancel
          </button>
          <button
            @click="saveEdit"
            :disabled="!editName.trim()"
            class="px-4 py-2 text-sm bg-shiraz text-white rounded hover:bg-opacity-90 disabled:opacity-50"
          >
            Save
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
