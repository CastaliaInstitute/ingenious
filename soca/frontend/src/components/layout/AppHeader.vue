<script setup lang="ts">
  import { useAuthStore } from '@/stores/auth'
  import { useUIStore } from '@/stores/ui'
  import type { TabName } from '@/types'

  const authStore = useAuthStore()
  const uiStore = useUIStore()

  const tabs: { name: TabName; label: string }[] = [
    { name: 'evaluations', label: 'Evaluations' },
    { name: 'submissions', label: 'Submissions' },
    { name: 'criteria', label: 'Criteria' },
  ]

  function handleTabClick(tab: TabName) {
    uiStore.setActiveTab(tab)
  }
</script>

<template>
  <header class="bg-white border-b border-gray-200">
    <div class="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
      <div class="flex items-center gap-8">
        <div class="flex items-center gap-2">
          <svg class="w-6 h-6 text-shiraz" viewBox="0 0 24 24" fill="currentColor">
            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span class="text-lg font-semibold text-mine">SoCa</span>
        </div>
        <nav class="flex items-center gap-1">
          <button
            v-for="tab in tabs"
            :key="tab.name"
            :class="[
              'px-4 py-2 text-sm font-medium rounded-md',
              uiStore.activeTab === tab.name
                ? 'text-shiraz bg-shiraz/10'
                : 'text-taupe hover:text-mine hover:bg-desert',
            ]"
            @click="handleTabClick(tab.name)"
          >
            {{ tab.label }}
          </button>
        </nav>
      </div>
      <div class="flex items-center gap-4 text-sm text-taupe">
        <span>{{ authStore.user?.email }}</span>
        <button
          class="text-taupe hover:text-shiraz transition-colors"
          title="Sign out"
          @click="authStore.logout()"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
            />
          </svg>
        </button>
      </div>
    </div>
  </header>
</template>
