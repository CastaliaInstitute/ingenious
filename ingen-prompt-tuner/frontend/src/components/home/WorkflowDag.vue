<script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import { VueFlow, Position, Handle } from '@vue-flow/core'
  import { Background } from '@vue-flow/background'
  import { Controls } from '@vue-flow/controls'
  import '@vue-flow/core/dist/style.css'
  import '@vue-flow/core/dist/theme-default.css'
  import '@vue-flow/controls/dist/style.css'

  // Expose Position for template use
  const pos = Position

  // Node and edge type definitions
  interface CustomNode {
    id: string
    type: string
    position: { x: number; y: number }
    data: {
      label: string
      description?: string
      phase?: number
      isInput?: boolean
      isOutput?: boolean
      isParallel?: boolean
    }
    sourcePosition?: Position
    targetPosition?: Position
    style?: Record<string, string>
  }

  interface CustomEdge {
    id: string
    source: string
    target: string
    type?: string
    animated?: boolean
    style?: Record<string, string>
    markerEnd?: string
  }

  // Helper functions for node styling
  function getNodeClasses(data: { phase?: number; isParallel?: boolean; label?: string }): string {
    if (data.label === 'Merge') {
      return 'border-gray-400 bg-gray-100'
    }
    if (data.phase === 4) {
      return 'border-green-400 bg-gradient-to-br from-green-50 to-green-100'
    }
    if (data.isParallel) {
      return 'border-shiraz/40 bg-gradient-to-br from-shiraz/5 to-shiraz/10'
    }
    return 'border-shiraz bg-white'
  }

  function getPhaseClasses(phase: number, isParallel?: boolean): string {
    if (phase === 4) {
      return 'bg-green-100 text-green-700'
    }
    if (isParallel) {
      return 'bg-shiraz/10 text-shiraz'
    }
    return 'bg-shiraz/20 text-shiraz'
  }

  // SoCa Evaluator nodes - clean layout with proper spacing
  const socaNodes = ref<CustomNode[]>([
    // Input node - centered vertically with middle agent
    {
      id: 'input',
      type: 'input',
      position: { x: 0, y: 140 },
      data: { label: 'Input', description: 'Submission + Criteria', isInput: true },
      sourcePosition: Position.Right,
    },
    // Phase 1 - Parallel agents with good vertical spacing
    {
      id: 'submission-eval',
      type: 'default',
      position: { x: 200, y: 0 },
      data: {
        label: 'Submission Evaluator',
        description: 'Analyzes document content',
        phase: 1,
        isParallel: true,
      },
      sourcePosition: Position.Right,
      targetPosition: Position.Left,
    },
    {
      id: 'criteria-eval',
      type: 'default',
      position: { x: 200, y: 140 },
      data: {
        label: 'Criteria Evaluator',
        description: 'Parses scoring rubrics',
        phase: 1,
        isParallel: true,
      },
      sourcePosition: Position.Right,
      targetPosition: Position.Left,
    },
    {
      id: 'next-steps',
      type: 'default',
      position: { x: 200, y: 280 },
      data: {
        label: 'Next Steps Agent',
        description: 'Identifies improvements',
        phase: 1,
        isParallel: true,
      },
      sourcePosition: Position.Right,
      targetPosition: Position.Left,
    },
    // Merge point - aligned with middle row, more space from parallel agents
    {
      id: 'merge',
      type: 'default',
      position: { x: 450, y: 140 },
      data: { label: 'Merge', description: 'Combine results' },
      sourcePosition: Position.Right,
      targetPosition: Position.Left,
    },
    // Phase 2-4 - all on same horizontal line (y=140) for straight connections
    {
      id: 'scoring',
      type: 'default',
      position: { x: 620, y: 140 },
      data: { label: 'Scoring Agent', description: 'Scores each criterion', phase: 2 },
      sourcePosition: Position.Right,
      targetPosition: Position.Left,
    },
    {
      id: 'summarizer',
      type: 'default',
      position: { x: 810, y: 140 },
      data: { label: 'Summarizer Agent', description: 'Creates summary', phase: 3 },
      sourcePosition: Position.Right,
      targetPosition: Position.Left,
    },
    {
      id: 'sanity-check',
      type: 'default',
      position: { x: 1010, y: 140 },
      data: { label: 'Sanity Check', description: 'Validates output', phase: 4 },
      sourcePosition: Position.Right,
      targetPosition: Position.Left,
    },
    // Output node - same y level
    {
      id: 'output',
      type: 'output',
      position: { x: 1190, y: 140 },
      data: { label: 'Result', description: 'Evaluation complete', isOutput: true },
      targetPosition: Position.Left,
    },
  ])

  // SoCa Evaluator edges - smoothstep for clean orthogonal routing
  const socaEdges = ref<CustomEdge[]>([
    // Input to parallel agents - smoothstep for clean fan-out
    {
      id: 'e-input-sub',
      source: 'input',
      target: 'submission-eval',
      type: 'smoothstep',
      animated: true,
    },
    {
      id: 'e-input-crit',
      source: 'input',
      target: 'criteria-eval',
      type: 'straight',
      animated: true,
    },
    {
      id: 'e-input-next',
      source: 'input',
      target: 'next-steps',
      type: 'smoothstep',
      animated: true,
    },
    // Parallel agents to merge - smoothstep for clean fan-in
    { id: 'e-sub-merge', source: 'submission-eval', target: 'merge', type: 'smoothstep' },
    { id: 'e-crit-merge', source: 'criteria-eval', target: 'merge', type: 'straight' },
    { id: 'e-next-merge', source: 'next-steps', target: 'merge', type: 'smoothstep' },
    // Sequential flow - straight lines (all same Y level)
    { id: 'e-merge-score', source: 'merge', target: 'scoring', type: 'straight', animated: true },
    {
      id: 'e-score-sum',
      source: 'scoring',
      target: 'summarizer',
      type: 'straight',
      animated: true,
    },
    {
      id: 'e-sum-sanity',
      source: 'summarizer',
      target: 'sanity-check',
      type: 'straight',
      animated: true,
    },
    {
      id: 'e-sanity-out',
      source: 'sanity-check',
      target: 'output',
      type: 'straight',
      animated: true,
    },
  ])

  // Criteria Generator nodes - wider spacing
  const criteriaNodes = ref<CustomNode[]>([
    {
      id: 'crit-input',
      type: 'input',
      position: { x: 0, y: 60 },
      data: { label: 'Document', description: 'Source document', isInput: true },
      sourcePosition: Position.Right,
    },
    {
      id: 'crit-gen',
      type: 'default',
      position: { x: 280, y: 60 },
      data: { label: 'Criteria Generator', description: 'AI extraction', phase: 1 },
      sourcePosition: Position.Right,
      targetPosition: Position.Left,
    },
    {
      id: 'crit-output',
      type: 'output',
      position: { x: 560, y: 60 },
      data: { label: 'Criteria Set', description: 'Generated criteria', isOutput: true },
      targetPosition: Position.Left,
    },
  ])

  const criteriaEdges = ref<CustomEdge[]>([
    {
      id: 'e-crit-in',
      source: 'crit-input',
      target: 'crit-gen',
      type: 'straight',
      animated: true,
    },
    {
      id: 'e-crit-out',
      source: 'crit-gen',
      target: 'crit-output',
      type: 'straight',
      animated: true,
    },
  ])

  // Active workflow tab
  const activeWorkflow = ref<'soca' | 'criteria'>('soca')

  // Fit view on mount
  const socaFlowRef = ref()
  const criteriaFlowRef = ref()

  onMounted(() => {
    setTimeout(() => {
      socaFlowRef.value?.fitView({ padding: 0.15 })
      criteriaFlowRef.value?.fitView({ padding: 0.4 })
    }, 100)
  })
</script>

<template>
  <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
    <!-- Header -->
    <div class="px-6 py-4 border-b border-gray-100 bg-gradient-to-r from-gray-50 to-white">
      <h3 class="text-base font-semibold text-mine">Workflow Architecture</h3>
      <p class="text-xs text-taupe mt-0.5">AI agent pipelines for document evaluation</p>
    </div>

    <!-- Workflow Tabs -->
    <div class="px-6 pt-4 border-b border-gray-100">
      <div class="flex gap-2">
        <button
          class="px-4 py-2 text-sm font-medium rounded-t-lg transition-colors"
          :class="
            activeWorkflow === 'soca'
              ? 'bg-shiraz text-white'
              : 'bg-gray-100 text-taupe hover:bg-gray-200'
          "
          @click="activeWorkflow = 'soca'"
        >
          <span class="flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
              />
            </svg>
            SoCa Evaluator
            <span
              class="text-xs px-1.5 py-0.5 rounded-full"
              :class="activeWorkflow === 'soca' ? 'bg-white/20' : 'bg-shiraz/10 text-shiraz'"
              >6 agents</span
            >
          </span>
        </button>
        <button
          class="px-4 py-2 text-sm font-medium rounded-t-lg transition-colors"
          :class="
            activeWorkflow === 'criteria'
              ? 'bg-taupe text-white'
              : 'bg-gray-100 text-taupe hover:bg-gray-200'
          "
          @click="activeWorkflow = 'criteria'"
        >
          <span class="flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
              />
            </svg>
            Criteria Generator
            <span
              class="text-xs px-1.5 py-0.5 rounded-full"
              :class="activeWorkflow === 'criteria' ? 'bg-white/20' : 'bg-taupe/10 text-taupe'"
              >1 agent</span
            >
          </span>
        </button>
      </div>
    </div>

    <!-- Flow Diagrams -->
    <div class="p-4">
      <!-- SoCa Evaluator Flow -->
      <div v-show="activeWorkflow === 'soca'" class="h-[450px] bg-gray-50 rounded-xl">
        <VueFlow
          ref="socaFlowRef"
          :nodes="socaNodes"
          :edges="socaEdges"
          :default-viewport="{ zoom: 0.6, x: 30, y: 30 }"
          :min-zoom="0.3"
          :max-zoom="1.5"
          fit-view-on-init
          :nodes-draggable="false"
          :nodes-connectable="false"
          :elements-selectable="false"
          :pan-on-drag="true"
          :zoom-on-scroll="true"
        >
          <Background pattern-color="#e5e7eb" :gap="16" />
          <Controls position="bottom-right" />

          <!-- Custom Node Template -->
          <template #node-default="{ data }">
            <div
              class="px-3 py-2 rounded-lg border-2 shadow-sm min-w-[140px] text-center transition-all relative"
              :class="getNodeClasses(data)"
            >
              <Handle type="target" :position="pos.Left" class="!bg-shiraz !w-2 !h-2" />
              <Handle type="source" :position="pos.Right" class="!bg-shiraz !w-2 !h-2" />
              <div class="text-xs font-semibold text-mine">
                {{ data.label }}
              </div>
              <div v-if="data.description" class="text-[10px] text-taupe mt-0.5">
                {{ data.description }}
              </div>
              <div
                v-if="data.phase"
                class="mt-1 text-[9px] font-medium px-1.5 py-0.5 rounded-full inline-block"
                :class="getPhaseClasses(data.phase, data.isParallel)"
              >
                Phase {{ data.phase }}{{ data.isParallel ? ' (Parallel)' : '' }}
              </div>
            </div>
          </template>

          <!-- Input Node Template -->
          <template #node-input="{ data }">
            <div
              class="px-4 py-3 rounded-xl border-2 border-gray-300 bg-white shadow-md min-w-[100px] text-center relative"
            >
              <Handle type="source" :position="pos.Right" class="!bg-gray-400 !w-2 !h-2" />
              <div
                class="w-8 h-8 mx-auto mb-1 rounded-lg bg-gray-100 flex items-center justify-center"
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
                    stroke-width="1.5"
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
              </div>
              <div class="text-xs font-semibold text-mine">
                {{ data.label }}
              </div>
              <div v-if="data.description" class="text-[10px] text-taupe">
                {{ data.description }}
              </div>
            </div>
          </template>

          <!-- Output Node Template -->
          <template #node-output="{ data }">
            <div
              class="px-4 py-3 rounded-xl border-2 border-green-400 bg-gradient-to-br from-green-50 to-green-100 shadow-md min-w-[100px] text-center relative"
            >
              <Handle type="target" :position="pos.Left" class="!bg-green-500 !w-2 !h-2" />
              <div
                class="w-8 h-8 mx-auto mb-1 rounded-lg bg-green-500 flex items-center justify-center"
              >
                <svg
                  class="w-5 h-5 text-white"
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
              <div class="text-xs font-semibold text-green-700">
                {{ data.label }}
              </div>
              <div v-if="data.description" class="text-[10px] text-green-600">
                {{ data.description }}
              </div>
            </div>
          </template>
        </VueFlow>
      </div>

      <!-- Criteria Generator Flow -->
      <div v-show="activeWorkflow === 'criteria'" class="h-[250px] bg-gray-50 rounded-xl">
        <VueFlow
          ref="criteriaFlowRef"
          :nodes="criteriaNodes"
          :edges="criteriaEdges"
          :default-viewport="{ zoom: 0.9, x: 50, y: 30 }"
          :min-zoom="0.5"
          :max-zoom="1.5"
          fit-view-on-init
          :nodes-draggable="false"
          :nodes-connectable="false"
          :elements-selectable="false"
          :pan-on-drag="true"
          :zoom-on-scroll="true"
        >
          <Background pattern-color="#e5e7eb" :gap="16" />
          <Controls position="bottom-right" />

          <!-- Custom Node Template -->
          <template #node-default="{ data }">
            <div
              class="px-4 py-3 rounded-lg border-2 border-taupe/30 bg-white shadow-sm min-w-[160px] text-center relative"
            >
              <Handle type="target" :position="pos.Left" class="!bg-taupe !w-2 !h-2" />
              <Handle type="source" :position="pos.Right" class="!bg-taupe !w-2 !h-2" />
              <div class="text-sm font-semibold text-mine">
                {{ data.label }}
              </div>
              <div v-if="data.description" class="text-xs text-taupe mt-0.5">
                {{ data.description }}
              </div>
            </div>
          </template>

          <!-- Input Node Template -->
          <template #node-input="{ data }">
            <div
              class="px-4 py-3 rounded-xl border-2 border-gray-300 bg-white shadow-md min-w-[100px] text-center relative"
            >
              <Handle type="source" :position="pos.Right" class="!bg-gray-400 !w-2 !h-2" />
              <div
                class="w-8 h-8 mx-auto mb-1 rounded-lg bg-gray-100 flex items-center justify-center"
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
                    stroke-width="1.5"
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
              </div>
              <div class="text-xs font-semibold text-mine">
                {{ data.label }}
              </div>
              <div v-if="data.description" class="text-[10px] text-taupe">
                {{ data.description }}
              </div>
            </div>
          </template>

          <!-- Output Node Template -->
          <template #node-output="{ data }">
            <div
              class="px-4 py-3 rounded-xl border-2 border-green-400 bg-gradient-to-br from-green-50 to-green-100 shadow-md min-w-[100px] text-center relative"
            >
              <Handle type="target" :position="pos.Left" class="!bg-green-500 !w-2 !h-2" />
              <div
                class="w-8 h-8 mx-auto mb-1 rounded-lg bg-green-500 flex items-center justify-center"
              >
                <svg
                  class="w-5 h-5 text-white"
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
              <div class="text-xs font-semibold text-green-700">
                {{ data.label }}
              </div>
              <div v-if="data.description" class="text-[10px] text-green-600">
                {{ data.description }}
              </div>
            </div>
          </template>
        </VueFlow>
      </div>
    </div>

    <!-- Legend -->
    <div class="px-6 py-3 bg-gray-50 border-t border-gray-100">
      <div class="flex flex-wrap items-center gap-4 text-xs text-taupe">
        <div class="flex items-center gap-1.5">
          <div class="w-3 h-3 rounded border-2 border-gray-300 bg-white" />
          <span>Input/Output</span>
        </div>
        <div class="flex items-center gap-1.5">
          <div class="w-3 h-3 rounded border-2 border-shiraz/40 bg-shiraz/10" />
          <span>Parallel Agent</span>
        </div>
        <div class="flex items-center gap-1.5">
          <div class="w-3 h-3 rounded border-2 border-shiraz bg-white" />
          <span>Sequential Agent</span>
        </div>
        <div class="flex items-center gap-1.5">
          <div class="w-3 h-3 rounded border-2 border-green-400 bg-green-100" />
          <span>Validation</span>
        </div>
        <div class="flex items-center gap-1.5">
          <div class="w-8 h-0.5 bg-shiraz/60 relative">
            <div
              class="absolute right-0 top-1/2 -translate-y-1/2 w-1.5 h-1.5 bg-shiraz/60 rounded-full animate-pulse"
            />
          </div>
          <span>Animated = Active Flow</span>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div class="px-6 py-3 bg-gray-50 border-t border-gray-100">
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

<style>
  /* Vue Flow customizations */
  .vue-flow__edge-path {
    stroke: #ae0a46;
    stroke-width: 2;
  }

  .vue-flow__edge.animated .vue-flow__edge-path {
    stroke-dasharray: 5;
    animation: dash 0.5s linear infinite;
  }

  @keyframes dash {
    to {
      stroke-dashoffset: -10;
    }
  }

  .vue-flow__controls {
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    overflow: hidden;
  }

  .vue-flow__controls-button {
    background: white;
    border: none;
    padding: 6px;
  }

  .vue-flow__controls-button:hover {
    background: #f3f4f6;
  }

  .vue-flow__background {
    background-color: #fafafa;
  }
</style>
