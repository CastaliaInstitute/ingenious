<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true

  try {
    await authStore.login(email.value, password.value)
  } catch (e) {
    error.value = 'Invalid email or password'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-desert flex items-center justify-center px-4">
    <div class="max-w-md w-full">
      <div class="bg-white rounded-lg border border-gray-200 p-8 shadow-sm">
        <div class="text-center mb-8">
          <div class="flex items-center justify-center gap-2 mb-2">
            <svg class="w-8 h-8 text-shiraz" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2L2 7v10l10 5 10-5V7L12 2zm0 2.5L18.5 7 12 9.5 5.5 7 12 4.5zM4 8.5l7 3.5v7l-7-3.5v-7zm9 10.5v-7l7-3.5v7l-7 3.5z"/>
            </svg>
            <span class="text-2xl font-semibold text-mine">SoCa</span>
          </div>
          <p class="text-taupe">Sign in to your account</p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label for="email" class="block text-sm font-medium text-mine mb-1">
              Email
            </label>
            <input
              id="email"
              v-model="email"
              type="email"
              required
              autocomplete="email"
              class="w-full px-3 py-2 border border-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-shiraz focus:border-transparent"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-mine mb-1">
              Password
            </label>
            <input
              id="password"
              v-model="password"
              type="password"
              required
              autocomplete="current-password"
              class="w-full px-3 py-2 border border-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-shiraz focus:border-transparent"
              placeholder="Enter your password"
            />
          </div>

          <div v-if="error" class="text-red-600 text-sm text-center">
            {{ error }}
          </div>

          <button
            type="submit"
            :disabled="loading || !email || !password"
            class="w-full bg-shiraz text-white py-2 px-4 rounded-md hover:bg-opacity-90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading">Signing in...</span>
            <span v-else>Sign In</span>
          </button>
        </form>

      </div>
    </div>
  </div>
</template>
