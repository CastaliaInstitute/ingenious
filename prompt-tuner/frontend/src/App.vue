<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import MainLayout from '@/components/layout/MainLayout.vue'
import HomePage from '@/components/home/HomePage.vue'
import PromptsPage from '@/components/prompts/PromptsPage.vue'
import TestPage from '@/components/test/TestPage.vue'

const authStore = useAuthStore()
const uiStore = useUIStore()

onMounted(() => {
  authStore.checkAuth()
})
</script>

<template>
  <MainLayout>
    <HomePage v-if="uiStore.activeTab === 'home'" />
    <PromptsPage v-else-if="uiStore.activeTab === 'prompts'" />
    <TestPage v-else-if="uiStore.activeTab === 'test'" />
  </MainLayout>
</template>
