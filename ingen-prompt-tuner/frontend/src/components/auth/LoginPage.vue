<script setup lang="ts">
  /**
   * LoginPage component for user authentication.
   * Displays a login form with email and password fields.
   */
  import { ref, computed } from 'vue'
  import { useAuthStore } from '@/stores/auth'

  const authStore = useAuthStore()

  const email = ref('')
  const password = ref('')
  const error = ref('')
  const loading = ref(false)

  const isFormValid = computed(() => email.value.trim() !== '' && password.value !== '')

  /**
   * Handles the login form submission.
   * Authenticates the user with provided credentials.
   */
  async function handleLogin() {
    error.value = ''
    loading.value = true

    try {
      await authStore.login(email.value, password.value)
    } catch {
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
              <path
                d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"
              />
            </svg>
            <span class="text-2xl font-semibold text-mine">Prompt Tuner</span>
          </div>
          <p class="text-taupe">Sign in to your account</p>
        </div>

        <form class="space-y-4" @submit.prevent="handleLogin">
          <div>
            <label for="email" class="block text-sm font-medium text-mine mb-1"> Email </label>
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
            :disabled="loading || !isFormValid"
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
