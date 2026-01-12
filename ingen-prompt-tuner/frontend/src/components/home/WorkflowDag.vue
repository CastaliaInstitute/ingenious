<script setup lang="ts">
  // Workflow DAG visualization showing the 6-agent pipeline for SoCa Evaluator
  // and single-agent flow for Criteria Generator

  const socaAgents = [
    { name: 'Submission Evaluator', phase: 1, description: 'Analyzes submission content' },
    { name: 'Criteria Evaluator', phase: 1, description: 'Parses criteria into rubrics' },
    { name: 'Next Steps Agent', phase: 1, description: 'Identifies improvements' },
    { name: 'Scoring Agent', phase: 2, description: 'Scores against criteria' },
    { name: 'Summarizer Agent', phase: 3, description: 'Creates executive summary' },
    { name: 'Sanity Check Agent', phase: 4, description: 'Validates consistency' },
  ]
</script>

<template>
  <div class="bg-white rounded-lg border border-gray-200 p-5">
    <h3 class="text-sm font-medium text-mine mb-4">Workflow Overview</h3>

    <!-- SoCa Evaluator - 6 Agent Pipeline -->
    <div class="mb-6">
      <div class="flex items-center gap-2 mb-3">
        <div class="w-3 h-3 rounded-full" style="background-color: #ae0a46"></div>
        <span class="text-sm font-medium text-mine">SoCa Evaluator</span>
        <span class="text-xs px-2 py-0.5 bg-shiraz/10 text-shiraz rounded-full">6 agents</span>
      </div>

      <!-- Pipeline Visualization -->
      <div class="bg-desert/30 rounded-lg p-4 overflow-x-auto">
        <div class="min-w-[700px]">
          <!-- Phase 1: Parallel Agents -->
          <div class="flex items-start gap-2 mb-3">
            <!-- Input -->
            <div class="flex-shrink-0 flex flex-col items-center w-16">
              <div
                class="w-10 h-10 rounded-lg bg-white border border-gray-200 flex items-center justify-center"
              >
                <svg
                  class="w-5 h-5 text-taupe"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
              </div>
              <span class="text-xs text-taupe mt-1">Input</span>
            </div>

            <!-- Arrows to parallel agents -->
            <div class="flex-shrink-0 flex flex-col justify-center h-24">
              <svg class="w-6 h-24" viewBox="0 0 24 96">
                <path d="M0 48 L12 12 L24 12" fill="none" stroke="#d1d5db" stroke-width="2" />
                <path d="M0 48 L24 48" fill="none" stroke="#d1d5db" stroke-width="2" />
                <path d="M0 48 L12 84 L24 84" fill="none" stroke="#d1d5db" stroke-width="2" />
              </svg>
            </div>

            <!-- Phase 1 Agents (Parallel) -->
            <div class="flex flex-col gap-1">
              <span class="text-xs text-taupe mb-1">Phase 1 (Parallel)</span>
              <div
                v-for="agent in socaAgents.filter((a) => a.phase === 1)"
                :key="agent.name"
                class="flex items-center gap-2 px-3 py-1.5 bg-white rounded border border-shiraz/30 text-xs"
                :title="agent.description"
              >
                <div class="w-2 h-2 rounded-full bg-shiraz"></div>
                <span class="text-mine whitespace-nowrap">{{ agent.name }}</span>
              </div>
            </div>

            <!-- Arrows from parallel to scoring -->
            <div class="flex-shrink-0 flex flex-col justify-center h-24">
              <svg class="w-6 h-24" viewBox="0 0 24 96">
                <path d="M0 12 L12 12 L24 48" fill="none" stroke="#d1d5db" stroke-width="2" />
                <path d="M0 48 L24 48" fill="none" stroke="#d1d5db" stroke-width="2" />
                <path d="M0 84 L12 84 L24 48" fill="none" stroke="#d1d5db" stroke-width="2" />
              </svg>
            </div>

            <!-- Phase 2-4 Agents (Sequential) -->
            <div class="flex items-center gap-2">
              <div
                v-for="agent in socaAgents.filter((a) => a.phase > 1)"
                :key="agent.name"
                class="flex flex-col items-center"
              >
                <span class="text-xs text-taupe mb-1">Phase {{ agent.phase }}</span>
                <div
                  class="flex items-center gap-2 px-3 py-1.5 bg-white rounded border border-shiraz/30 text-xs"
                  :title="agent.description"
                >
                  <div class="w-2 h-2 rounded-full bg-shiraz"></div>
                  <span class="text-mine whitespace-nowrap">{{ agent.name }}</span>
                </div>
              </div>
            </div>

            <!-- Arrow to output -->
            <div class="flex-shrink-0 flex items-center h-24">
              <svg class="w-6 h-4" viewBox="0 0 24 16">
                <path
                  d="M0 8 L18 8 M14 4 L22 8 L14 12"
                  fill="none"
                  stroke="#d1d5db"
                  stroke-width="2"
                  stroke-linecap="round"
                />
              </svg>
            </div>

            <!-- Output -->
            <div class="flex-shrink-0 flex flex-col items-center w-16">
              <div
                class="w-10 h-10 rounded-lg bg-white border border-gray-200 flex items-center justify-center"
              >
                <svg
                  class="w-5 h-5 text-taupe"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <span class="text-xs text-taupe mt-1">Result</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Criteria Generator - Single Agent -->
    <div class="mb-4">
      <div class="flex items-center gap-2 mb-3">
        <div class="w-3 h-3 rounded-full" style="background-color: #3e332d"></div>
        <span class="text-sm font-medium text-mine">Criteria Generator</span>
        <span class="text-xs px-2 py-0.5 bg-taupe/10 text-taupe rounded-full">1 agent</span>
      </div>

      <!-- Simple Pipeline -->
      <div class="flex items-center gap-3 px-4">
        <div class="flex flex-col items-center">
          <div
            class="w-10 h-10 rounded-lg bg-white border border-gray-200 flex items-center justify-center"
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
          <span class="text-xs text-taupe mt-1">Document</span>
        </div>

        <svg class="w-8 h-4 text-gray-300" viewBox="0 0 32 16">
          <path
            d="M0 8 L24 8 M20 4 L28 8 L20 12"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
          />
        </svg>

        <div class="flex items-center gap-2 px-4 py-2 bg-white rounded-lg border border-taupe/30">
          <div class="w-2 h-2 rounded-full bg-taupe"></div>
          <span class="text-sm text-mine">Criteria Generator</span>
        </div>

        <svg class="w-8 h-4 text-gray-300" viewBox="0 0 32 16">
          <path
            d="M0 8 L24 8 M20 4 L28 8 L20 12"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
          />
        </svg>

        <div class="flex flex-col items-center">
          <div
            class="w-10 h-10 rounded-lg bg-white border border-gray-200 flex items-center justify-center"
          >
            <svg class="w-5 h-5 text-taupe" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
              />
            </svg>
          </div>
          <span class="text-xs text-taupe mt-1">Criteria</span>
        </div>
      </div>
    </div>

    <div class="pt-4 border-t border-gray-100">
      <p class="text-xs text-taupe">
        Client applications call the
        <code class="px-1 py-0.5 bg-desert rounded text-mine">/api/v1/chat</code> endpoint with a
        <code class="px-1 py-0.5 bg-desert rounded text-mine">conversation_flow</code> parameter to
        select the workflow.
      </p>
    </div>
  </div>
</template>
