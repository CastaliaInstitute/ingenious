<script setup lang="ts">
  // Static workflow DAG visualization
  // Shows available conversation flows and their structure

  const workflows = [
    {
      id: 'soca-evaluator',
      name: 'SoCa Evaluator',
      description: 'Evaluate submissions against criteria',
      color: '#AE0A46', // shiraz
    },
    {
      id: 'criteria-generator',
      name: 'Criteria Generator',
      description: 'Extract criteria from documents',
      color: '#3E332D', // taupe
    },
  ]
</script>

<template>
  <div class="bg-white rounded-lg border border-gray-200 p-5">
    <h3 class="text-sm font-medium text-mine mb-4">Workflow Overview</h3>

    <div class="space-y-4">
      <div v-for="workflow in workflows" :key="workflow.id" class="flex items-center gap-3">
        <!-- User Input Node -->
        <div class="flex-shrink-0 w-20 text-center">
          <div
            class="inline-flex items-center justify-center w-10 h-10 rounded-lg bg-desert border border-gray-200"
          >
            <svg class="w-5 h-5 text-taupe" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
              />
            </svg>
          </div>
          <p class="text-xs text-taupe mt-1">Input</p>
        </div>

        <!-- Arrow -->
        <svg class="w-8 h-4 text-gray-300 flex-shrink-0" viewBox="0 0 32 16">
          <path
            d="M0 8 L24 8 M20 4 L28 8 L20 12"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>

        <!-- Agent Node -->
        <div class="flex-1 min-w-0">
          <div
            class="flex items-center gap-3 px-4 py-3 rounded-lg border-2"
            :style="{ borderColor: workflow.color + '40', backgroundColor: workflow.color + '08' }"
          >
            <div
              class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center"
              :style="{ backgroundColor: workflow.color }"
            >
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                />
              </svg>
            </div>
            <div class="min-w-0">
              <p class="text-sm font-medium text-mine truncate">{{ workflow.name }}</p>
              <p class="text-xs text-taupe truncate">{{ workflow.description }}</p>
            </div>
          </div>
        </div>

        <!-- Arrow -->
        <svg class="w-8 h-4 text-gray-300 flex-shrink-0" viewBox="0 0 32 16">
          <path
            d="M0 8 L24 8 M20 4 L28 8 L20 12"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>

        <!-- Output Node -->
        <div class="flex-shrink-0 w-20 text-center">
          <div
            class="inline-flex items-center justify-center w-10 h-10 rounded-lg bg-desert border border-gray-200"
          >
            <svg class="w-5 h-5 text-taupe" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
          </div>
          <p class="text-xs text-taupe mt-1">JSON</p>
        </div>
      </div>
    </div>

    <div class="mt-4 pt-4 border-t border-gray-100">
      <p class="text-xs text-taupe">
        Client applications call the
        <code class="px-1 py-0.5 bg-desert rounded text-mine">/api/v1/chat</code> endpoint with a
        <code class="px-1 py-0.5 bg-desert rounded text-mine">conversation_flow</code> parameter to
        select the workflow.
      </p>
    </div>
  </div>
</template>
