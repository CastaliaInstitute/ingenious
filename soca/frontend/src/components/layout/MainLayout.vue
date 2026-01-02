<script setup lang="ts">
import AppHeader from './AppHeader.vue'
</script>

<template>
  <div class="min-h-screen bg-desert text-mine">
    <AppHeader />
    <main class="max-w-5xl mx-auto px-6 py-8">
      <slot />
    </main>
  </div>
</template>
