<script setup lang="ts">
  import { onMounted, ref } from 'vue'
  import { useAuthStore } from '@/stores/auth'
  import { useUIStore } from '@/stores/ui'
  import LoginPage from '@/components/auth/LoginPage.vue'
  import MainLayout from '@/components/layout/MainLayout.vue'
  import EvaluationsPage from '@/components/evaluations/EvaluationsPage.vue'
  import EvaluationResultsPage from '@/components/evaluations/EvaluationResultsPage.vue'
  import SubmissionsPage from '@/components/submissions/SubmissionsPage.vue'
  import CriteriaPage from '@/components/criteria/CriteriaPage.vue'
  import Spinner from '@/components/common/Spinner.vue'

  const authStore = useAuthStore()
  const uiStore = useUIStore()
  const initializing = ref(true)

  onMounted(async () => {
    await authStore.checkAuth()
    initializing.value = false
  })
</script>

<template>
  <div v-if="initializing" class="min-h-screen bg-desert flex items-center justify-center">
    <Spinner size="lg" text="Loading..." />
  </div>

  <LoginPage v-else-if="!authStore.isAuthenticated" />

  <MainLayout v-else>
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
