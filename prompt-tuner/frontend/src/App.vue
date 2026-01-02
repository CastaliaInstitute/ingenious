<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import LoginPage from '@/components/auth/LoginPage.vue'
import MainLayout from '@/components/layout/MainLayout.vue'
import HomePage from '@/components/home/HomePage.vue'
import PromptsPage from '@/components/prompts/PromptsPage.vue'
import TestPage from '@/components/test/TestPage.vue'

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
    <div class="text-taupe">Loading...</div>
  </div>

  <LoginPage v-else-if="!authStore.isAuthenticated" />

  <MainLayout v-else>
    <HomePage v-if="uiStore.activeTab === 'home'" />
    <PromptsPage v-else-if="uiStore.activeTab === 'prompts'" />
    <TestPage v-else-if="uiStore.activeTab === 'test'" />
  </MainLayout>
</template>
