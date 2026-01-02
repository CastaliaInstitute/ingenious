<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useSubmissionsStore } from '@/stores/submissions'
import Card from '@/components/common/Card.vue'
import UploadDropzone from './UploadDropzone.vue'
import SubmissionItem from './SubmissionItem.vue'

const submissionsStore = useSubmissionsStore()
const isDragging = ref(false)

onMounted(() => {
  submissionsStore.fetchSubmissions()
})

async function handleFilesSelected(files: File[]) {
  for (const file of files) {
    await submissionsStore.uploadSubmission(file, file.name)
  }
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

    <div v-if="submissionsStore.loading" class="text-center py-8 text-taupe">
      Loading submissions...
    </div>

    <div v-else-if="submissionsStore.error" class="text-center py-8 text-red-600">
      {{ submissionsStore.error }}
    </div>

    <div v-else class="space-y-3">
      <SubmissionItem
        v-for="submission in submissionsStore.submissions"
        :key="submission.id"
        :submission="submission"
        @delete="submissionsStore.deleteSubmission(submission.id)"
      />

      <div v-if="submissionsStore.submissions.length === 0" class="text-center py-8 text-taupe">
        No submissions yet. Upload your first document to get started.
      </div>
    </div>
  </div>
</template>
