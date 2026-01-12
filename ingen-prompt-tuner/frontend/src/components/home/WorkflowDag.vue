<script setup lang="ts">
  // Workflow DAG visualization showing the 6-agent pipeline for SoCa Evaluator
  // and single-agent flow for Criteria Generator

  interface Agent {
    name: string
    phase: number
    description: string
    icon: string
  }

  const socaAgents: Agent[] = [
    { name: 'Submission Evaluator', phase: 1, description: 'Analyzes content', icon: 'doc' },
    { name: 'Criteria Evaluator', phase: 1, description: 'Parses rubrics', icon: 'list' },
    { name: 'Next Steps Agent', phase: 1, description: 'Finds improvements', icon: 'lightbulb' },
    { name: 'Scoring Agent', phase: 2, description: 'Scores criteria', icon: 'star' },
    { name: 'Summarizer Agent', phase: 3, description: 'Creates summary', icon: 'summary' },
    { name: 'Sanity Check Agent', phase: 4, description: 'Validates output', icon: 'check' },
  ]

  const phase1Agents = socaAgents.filter((a) => a.phase === 1)
  const laterAgents = socaAgents.filter((a) => a.phase > 1)
</script>

<template>
  <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
    <!-- Header -->
    <div class="px-6 py-4 border-b border-gray-100 bg-gradient-to-r from-gray-50 to-white">
      <h3 class="text-base font-semibold text-mine">Workflow Architecture</h3>
      <p class="text-xs text-taupe mt-0.5">AI agent pipelines for document evaluation</p>
    </div>

    <div class="p-6 space-y-8">
      <!-- SoCa Evaluator Pipeline -->
      <div>
        <div class="flex items-center gap-3 mb-5">
          <div
            class="w-10 h-10 rounded-xl bg-gradient-to-br from-shiraz to-shiraz/80 flex items-center justify-center shadow-md"
          >
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
              />
            </svg>
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="text-sm font-semibold text-mine">SoCa Evaluator</span>
              <span class="text-xs px-2 py-0.5 bg-shiraz/10 text-shiraz rounded-full font-medium"
                >6 agents</span
              >
            </div>
            <p class="text-xs text-taupe">Multi-phase evaluation pipeline</p>
          </div>
        </div>

        <!-- Pipeline Visualization -->
        <div
          class="relative bg-gradient-to-br from-gray-50 via-white to-desert/20 rounded-xl border border-gray-100 p-6 overflow-x-auto"
        >
          <div class="flex items-stretch gap-4 min-w-[900px]">
            <!-- Input -->
            <div class="flex flex-col items-center justify-center">
              <div
                class="w-14 h-14 rounded-2xl bg-white border-2 border-gray-200 flex items-center justify-center shadow-sm"
              >
                <svg
                  class="w-7 h-7 text-taupe"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="1.5"
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
              </div>
              <span class="text-xs font-medium text-taupe mt-2">Input</span>
            </div>

            <!-- Connector -->
            <div class="flex items-center">
              <div class="w-8 h-0.5 bg-gradient-to-r from-gray-300 to-shiraz/40"></div>
              <div
                class="w-0 h-0 border-t-4 border-b-4 border-l-6 border-t-transparent border-b-transparent border-l-shiraz/40"
              ></div>
            </div>

            <!-- Phase 1: Parallel -->
            <div class="flex-shrink-0">
              <div class="text-center mb-3">
                <span
                  class="inline-flex items-center gap-1.5 px-3 py-1 bg-shiraz/10 text-shiraz text-xs font-semibold rounded-full"
                >
                  <span class="w-1.5 h-1.5 bg-shiraz rounded-full animate-pulse"></span>
                  Phase 1
                </span>
                <p class="text-xs text-taupe mt-1">Parallel Analysis</p>
              </div>
              <div class="relative bg-white rounded-xl border border-shiraz/20 p-3 shadow-sm">
                <div
                  class="absolute -left-1 top-1/2 -translate-y-1/2 w-2 h-12 bg-shiraz/20 rounded-r-full"
                ></div>
                <div class="space-y-2">
                  <div
                    v-for="agent in phase1Agents"
                    :key="agent.name"
                    class="flex items-center gap-2.5 px-3 py-2 bg-gradient-to-r from-shiraz/5 to-transparent rounded-lg border border-shiraz/10 hover:border-shiraz/30 transition-colors"
                  >
                    <div
                      class="w-7 h-7 rounded-lg bg-shiraz/10 flex items-center justify-center flex-shrink-0"
                    >
                      <div class="w-2 h-2 rounded-full bg-shiraz"></div>
                    </div>
                    <div class="min-w-0">
                      <p class="text-xs font-medium text-mine truncate">{{ agent.name }}</p>
                      <p class="text-xs text-taupe/70 truncate">{{ agent.description }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Connector with merge -->
            <div class="flex items-center">
              <div class="w-6 h-0.5 bg-gradient-to-r from-shiraz/40 to-shiraz/60"></div>
              <div class="w-4 h-4 rounded-full bg-shiraz/20 flex items-center justify-center">
                <div class="w-2 h-2 rounded-full bg-shiraz/60"></div>
              </div>
              <div class="w-6 h-0.5 bg-gradient-to-r from-shiraz/60 to-shiraz/40"></div>
            </div>

            <!-- Phases 2-4: Sequential -->
            <div class="flex items-center gap-3">
              <template v-for="(agent, index) in laterAgents" :key="agent.name">
                <div class="flex-shrink-0">
                  <div class="text-center mb-3">
                    <span
                      class="inline-flex items-center gap-1.5 px-3 py-1 text-xs font-semibold rounded-full"
                      :class="
                        agent.phase === 4
                          ? 'bg-green-100 text-green-700'
                          : 'bg-shiraz/10 text-shiraz'
                      "
                    >
                      Phase {{ agent.phase }}
                    </span>
                  </div>
                  <div
                    class="bg-white rounded-xl border p-3 shadow-sm min-w-[140px]"
                    :class="agent.phase === 4 ? 'border-green-200' : 'border-shiraz/20'"
                  >
                    <div
                      class="flex items-center gap-2.5 px-2 py-1.5 rounded-lg"
                      :class="agent.phase === 4 ? 'bg-green-50' : 'bg-shiraz/5'"
                    >
                      <div
                        class="w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0"
                        :class="agent.phase === 4 ? 'bg-green-100' : 'bg-shiraz/10'"
                      >
                        <div
                          class="w-2 h-2 rounded-full"
                          :class="agent.phase === 4 ? 'bg-green-600' : 'bg-shiraz'"
                        ></div>
                      </div>
                      <div class="min-w-0">
                        <p class="text-xs font-medium text-mine truncate">{{ agent.name }}</p>
                        <p class="text-xs text-taupe/70 truncate">{{ agent.description }}</p>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Connector between phases -->
                <div
                  v-if="index < laterAgents.length - 1"
                  class="flex items-center self-center mt-6"
                >
                  <div class="w-4 h-0.5 bg-shiraz/30"></div>
                  <svg class="w-3 h-3 text-shiraz/50" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fill-rule="evenodd"
                      d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </div>
              </template>
            </div>

            <!-- Connector to output -->
            <div class="flex items-center self-center mt-6">
              <div class="w-6 h-0.5 bg-gradient-to-r from-green-300 to-green-400"></div>
              <div
                class="w-0 h-0 border-t-4 border-b-4 border-l-6 border-t-transparent border-b-transparent border-l-green-400"
              ></div>
            </div>

            <!-- Output -->
            <div class="flex flex-col items-center justify-center self-center mt-6">
              <div
                class="w-14 h-14 rounded-2xl bg-gradient-to-br from-green-500 to-green-600 flex items-center justify-center shadow-lg shadow-green-500/20"
              >
                <svg
                  class="w-7 h-7 text-white"
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
              <span class="text-xs font-medium text-green-700 mt-2">Result</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Divider -->
      <div class="border-t border-gray-100"></div>

      <!-- Criteria Generator -->
      <div>
        <div class="flex items-center gap-3 mb-5">
          <div
            class="w-10 h-10 rounded-xl bg-gradient-to-br from-taupe to-taupe/80 flex items-center justify-center shadow-md"
          >
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
              />
            </svg>
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="text-sm font-semibold text-mine">Criteria Generator</span>
              <span class="text-xs px-2 py-0.5 bg-taupe/10 text-taupe rounded-full font-medium"
                >1 agent</span
              >
            </div>
            <p class="text-xs text-taupe">Extract criteria from documents</p>
          </div>
        </div>

        <!-- Simple Pipeline -->
        <div
          class="bg-gradient-to-br from-gray-50 via-white to-desert/20 rounded-xl border border-gray-100 p-6"
        >
          <div class="flex items-center gap-4">
            <!-- Document Input -->
            <div class="flex flex-col items-center">
              <div
                class="w-14 h-14 rounded-2xl bg-white border-2 border-gray-200 flex items-center justify-center shadow-sm"
              >
                <svg
                  class="w-7 h-7 text-taupe"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="1.5"
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
              </div>
              <span class="text-xs font-medium text-taupe mt-2">Document</span>
            </div>

            <!-- Connector -->
            <div class="flex items-center">
              <div class="w-12 h-0.5 bg-gradient-to-r from-gray-300 to-taupe/40"></div>
              <div
                class="w-0 h-0 border-t-4 border-b-4 border-l-6 border-t-transparent border-b-transparent border-l-taupe/40"
              ></div>
            </div>

            <!-- Agent -->
            <div class="bg-white rounded-xl border border-taupe/20 p-4 shadow-sm">
              <div class="flex items-center gap-3 px-2 py-1 bg-taupe/5 rounded-lg">
                <div class="w-9 h-9 rounded-lg bg-taupe/10 flex items-center justify-center">
                  <div class="w-2.5 h-2.5 rounded-full bg-taupe"></div>
                </div>
                <div>
                  <p class="text-sm font-medium text-mine">Criteria Generator</p>
                  <p class="text-xs text-taupe/70">AI extraction</p>
                </div>
              </div>
            </div>

            <!-- Connector -->
            <div class="flex items-center">
              <div class="w-12 h-0.5 bg-gradient-to-r from-taupe/40 to-green-400"></div>
              <div
                class="w-0 h-0 border-t-4 border-b-4 border-l-6 border-t-transparent border-b-transparent border-l-green-400"
              ></div>
            </div>

            <!-- Output -->
            <div class="flex flex-col items-center">
              <div
                class="w-14 h-14 rounded-2xl bg-gradient-to-br from-green-500 to-green-600 flex items-center justify-center shadow-lg shadow-green-500/20"
              >
                <svg
                  class="w-7 h-7 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
                  />
                </svg>
              </div>
              <span class="text-xs font-medium text-green-700 mt-2">Criteria</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div class="px-6 py-4 bg-gray-50 border-t border-gray-100">
      <div class="flex items-center gap-2 text-xs text-taupe">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <span>
          Call
          <code class="px-1.5 py-0.5 bg-white rounded border border-gray-200 font-mono text-mine"
            >/api/v1/chat</code
          >
          with
          <code class="px-1.5 py-0.5 bg-white rounded border border-gray-200 font-mono text-mine"
            >conversation_flow</code
          >
          to select workflow
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
  .border-l-6 {
    border-left-width: 6px;
  }
</style>
