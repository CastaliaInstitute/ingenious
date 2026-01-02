<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import type { TabName } from '@/types'

const authStore = useAuthStore()
const uiStore = useUIStore()

const tabs: { name: TabName; label: string }[] = [
  { name: 'home', label: 'Home' },
  { name: 'prompts', label: 'Prompts' },
  { name: 'test', label: 'Test' }
]

function handleTabClick(tab: TabName) {
  uiStore.setActiveTab(tab)
}
</script>

<template>
  <header class="bg-white border-b border-gray-200">
    <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
      <div class="flex items-center gap-8">
        <div class="flex items-center gap-2">
          <svg class="w-6 h-6 text-shiraz" viewBox="0 0 24 24" fill="currentColor">
            <rect x="2" y="2" width="9" height="9" rx="1" />
            <rect x="13" y="2" width="9" height="9" rx="1" />
            <rect x="2" y="13" width="9" height="9" rx="1" />
            <rect x="13" y="13" width="9" height="9" rx="1" opacity="0.5" />
          </svg>
          <span class="text-lg font-semibold text-mine">Prompt Tuner</span>
        </div>
        <nav class="flex items-center gap-1">
          <button
            v-for="tab in tabs"
            :key="tab.name"
            @click="handleTabClick(tab.name)"
            :class="[
              'px-4 py-2 text-sm font-medium rounded-md',
              uiStore.activeTab === tab.name
                ? 'text-shiraz bg-shiraz/10'
                : 'text-taupe hover:text-mine hover:bg-desert'
            ]"
          >
            {{ tab.label }}
          </button>
        </nav>
      </div>
      <div class="flex items-center gap-4 text-sm text-taupe">
        <span>{{ authStore.user?.email }}</span>
        <button
          @click="authStore.logout()"
          class="text-taupe hover:text-shiraz transition-colors"
          title="Sign out"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
        </button>
      </div>
    </div>
  </header>
</template>
