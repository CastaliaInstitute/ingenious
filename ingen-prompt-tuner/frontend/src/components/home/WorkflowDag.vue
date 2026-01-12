<script setup lang="ts">
  // Workflow DAG visualization showing the 6-agent pipeline for SoCa Evaluator
  // and single-agent flow for Criteria Generator
</script>

<template>
  <div class="bg-white rounded-lg border border-gray-200 p-5">
    <h3 class="text-sm font-medium text-mine mb-4">Workflow Overview</h3>

    <!-- SoCa Evaluator - 6 Agent Pipeline -->
    <div class="mb-6">
      <div class="flex items-center gap-2 mb-4">
        <div class="w-3 h-3 rounded-full bg-shiraz"></div>
        <span class="text-sm font-medium text-mine">SoCa Evaluator</span>
        <span class="text-xs px-2 py-0.5 bg-shiraz/10 text-shiraz rounded-full font-medium"
          >6 agents</span
        >
      </div>

      <!-- Pipeline Visualization - Clean horizontal layout -->
      <div class="bg-desert/20 rounded-lg p-5 overflow-x-auto">
        <div class="flex items-center gap-3 min-w-[780px]">
          <!-- Input Node -->
          <div class="flex flex-col items-center flex-shrink-0">
            <div
              class="w-12 h-12 rounded-lg bg-white border-2 border-gray-200 flex items-center justify-center shadow-sm"
            >
              <svg class="w-6 h-6 text-taupe" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.5"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
            </div>
            <span class="text-xs text-taupe mt-1.5 font-medium">Input</span>
          </div>

          <!-- Arrow to Phase 1 -->
          <svg class="w-8 h-6 flex-shrink-0 text-gray-300" viewBox="0 0 32 24">
            <path
              d="M0 12 L24 12 M20 8 L28 12 L20 16"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>

          <!-- Phase 1: Parallel Agents -->
          <div class="flex flex-col gap-2 flex-shrink-0">
            <div class="flex items-center gap-1.5 mb-1">
              <span class="text-xs font-semibold text-shiraz/80">Phase 1</span>
              <span class="text-xs text-taupe">(Parallel)</span>
            </div>
            <div
              class="flex items-center gap-2 px-3 py-2 bg-white rounded-md border border-shiraz/20 shadow-sm"
            >
              <div class="w-2 h-2 rounded-full bg-shiraz"></div>
              <span class="text-xs text-mine font-medium">Submission Evaluator</span>
            </div>
            <div
              class="flex items-center gap-2 px-3 py-2 bg-white rounded-md border border-shiraz/20 shadow-sm"
            >
              <div class="w-2 h-2 rounded-full bg-shiraz"></div>
              <span class="text-xs text-mine font-medium">Criteria Evaluator</span>
            </div>
            <div
              class="flex items-center gap-2 px-3 py-2 bg-white rounded-md border border-shiraz/20 shadow-sm"
            >
              <div class="w-2 h-2 rounded-full bg-shiraz"></div>
              <span class="text-xs text-mine font-medium">Next Steps Agent</span>
            </div>
          </div>

          <!-- Arrow to Phase 2 -->
          <svg class="w-8 h-6 flex-shrink-0 text-gray-300" viewBox="0 0 32 24">
            <path
              d="M0 12 L24 12 M20 8 L28 12 L20 16"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>

          <!-- Phase 2: Scoring Agent -->
          <div class="flex flex-col flex-shrink-0">
            <span class="text-xs font-semibold text-shiraz/80 mb-1">Phase 2</span>
            <div
              class="flex items-center gap-2 px-3 py-2 bg-white rounded-md border border-shiraz/20 shadow-sm"
            >
              <div class="w-2 h-2 rounded-full bg-shiraz"></div>
              <span class="text-xs text-mine font-medium">Scoring Agent</span>
            </div>
          </div>

          <!-- Arrow to Phase 3 -->
          <svg class="w-8 h-6 flex-shrink-0 text-gray-300" viewBox="0 0 32 24">
            <path
              d="M0 12 L24 12 M20 8 L28 12 L20 16"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>

          <!-- Phase 3: Summarizer Agent -->
          <div class="flex flex-col flex-shrink-0">
            <span class="text-xs font-semibold text-shiraz/80 mb-1">Phase 3</span>
            <div
              class="flex items-center gap-2 px-3 py-2 bg-white rounded-md border border-shiraz/20 shadow-sm"
            >
              <div class="w-2 h-2 rounded-full bg-shiraz"></div>
              <span class="text-xs text-mine font-medium">Summarizer Agent</span>
            </div>
          </div>

          <!-- Arrow to Phase 4 -->
          <svg class="w-8 h-6 flex-shrink-0 text-gray-300" viewBox="0 0 32 24">
            <path
              d="M0 12 L24 12 M20 8 L28 12 L20 16"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>

          <!-- Phase 4: Sanity Check Agent -->
          <div class="flex flex-col flex-shrink-0">
            <span class="text-xs font-semibold text-shiraz/80 mb-1">Phase 4</span>
            <div
              class="flex items-center gap-2 px-3 py-2 bg-white rounded-md border border-shiraz/20 shadow-sm"
            >
              <div class="w-2 h-2 rounded-full bg-shiraz"></div>
              <span class="text-xs text-mine font-medium">Sanity Check Agent</span>
            </div>
          </div>

          <!-- Arrow to Output -->
          <svg class="w-8 h-6 flex-shrink-0 text-gray-300" viewBox="0 0 32 24">
            <path
              d="M0 12 L24 12 M20 8 L28 12 L20 16"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>

          <!-- Output Node -->
          <div class="flex flex-col items-center flex-shrink-0">
            <div
              class="w-12 h-12 rounded-lg bg-white border-2 border-green-200 flex items-center justify-center shadow-sm"
            >
              <svg
                class="w-6 h-6 text-green-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.5"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <span class="text-xs text-taupe mt-1.5 font-medium">Result</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Criteria Generator - Single Agent -->
    <div class="mb-4">
      <div class="flex items-center gap-2 mb-4">
        <div class="w-3 h-3 rounded-full bg-taupe"></div>
        <span class="text-sm font-medium text-mine">Criteria Generator</span>
        <span class="text-xs px-2 py-0.5 bg-taupe/10 text-taupe rounded-full font-medium"
          >1 agent</span
        >
      </div>

      <!-- Simple Pipeline -->
      <div class="bg-desert/20 rounded-lg p-5">
        <div class="flex items-center gap-3">
          <!-- Document Input -->
          <div class="flex flex-col items-center">
            <div
              class="w-12 h-12 rounded-lg bg-white border-2 border-gray-200 flex items-center justify-center shadow-sm"
            >
              <svg class="w-6 h-6 text-taupe" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.5"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
            </div>
            <span class="text-xs text-taupe mt-1.5 font-medium">Document</span>
          </div>

          <!-- Arrow -->
          <svg class="w-8 h-6 text-gray-300" viewBox="0 0 32 24">
            <path
              d="M0 12 L24 12 M20 8 L28 12 L20 16"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>

          <!-- Agent -->
          <div
            class="flex items-center gap-2 px-4 py-2.5 bg-white rounded-md border border-taupe/20 shadow-sm"
          >
            <div class="w-2 h-2 rounded-full bg-taupe"></div>
            <span class="text-sm text-mine font-medium">Criteria Generator</span>
          </div>

          <!-- Arrow -->
          <svg class="w-8 h-6 text-gray-300" viewBox="0 0 32 24">
            <path
              d="M0 12 L24 12 M20 8 L28 12 L20 16"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>

          <!-- Criteria Output -->
          <div class="flex flex-col items-center">
            <div
              class="w-12 h-12 rounded-lg bg-white border-2 border-green-200 flex items-center justify-center shadow-sm"
            >
              <svg
                class="w-6 h-6 text-green-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.5"
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
                />
              </svg>
            </div>
            <span class="text-xs text-taupe mt-1.5 font-medium">Criteria</span>
          </div>
        </div>
      </div>
    </div>

    <div class="pt-4 border-t border-gray-100">
      <p class="text-xs text-taupe">
        Client applications call the
        <code class="px-1.5 py-0.5 bg-desert rounded text-mine font-mono text-xs"
          >/api/v1/chat</code
        >
        endpoint with a
        <code class="px-1.5 py-0.5 bg-desert rounded text-mine font-mono text-xs"
          >conversation_flow</code
        >
        parameter to select the workflow.
      </p>
    </div>
  </div>
</template>
