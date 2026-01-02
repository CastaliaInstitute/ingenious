<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import MainLayout from '@/components/layout/MainLayout.vue'
import EvaluationsPage from '@/components/evaluations/EvaluationsPage.vue'
import EvaluationResultsPage from '@/components/evaluations/EvaluationResultsPage.vue'
import SubmissionsPage from '@/components/submissions/SubmissionsPage.vue'
import CriteriaPage from '@/components/criteria/CriteriaPage.vue'

const authStore = useAuthStore()
const uiStore = useUIStore()

onMounted(() => {
  authStore.checkAuth()
})
</script>

<template>
  <MainLayout>
    <template v-if="uiStore.selectedEvaluationId">
      <EvaluationResultsPage />
    </template>
    <template v-else>
      <EvaluationsPage v-if="uiStore.activeTab === 'evaluations'" />
      <SubmissionsPage v-else-if="uiStore.activeTab === 'submissions'" />
      <CriteriaPage v-else-if="uiStore.activeTab === 'criteria'" />
    </template>
  </MainLayout>
</template>
