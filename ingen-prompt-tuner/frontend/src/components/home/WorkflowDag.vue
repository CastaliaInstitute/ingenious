<script setup lang="ts">
  import { ref, onMounted, watch, nextTick } from 'vue'
  import mermaid from 'mermaid'

  // Initialize mermaid with custom theme
  mermaid.initialize({
    startOnLoad: false,
    theme: 'base',
    themeVariables: {
      primaryColor: '#fff',
      primaryTextColor: '#222222',
      primaryBorderColor: '#AE0A46',
      lineColor: '#AE0A46',
      secondaryColor: '#F7F6F5',
      tertiaryColor: '#fff',
      fontFamily: 'Inter, system-ui, sans-serif',
      fontSize: '12px',
    },
    flowchart: {
      curve: 'basis',
      padding: 20,
      nodeSpacing: 50,
      rankSpacing: 60,
      htmlLabels: true,
    },
  })

  // Active workflow tab
  const activeWorkflow = ref<'soca' | 'criteria'>('soca')

  // Container refs
  const socaContainer = ref<HTMLElement | null>(null)
  const criteriaContainer = ref<HTMLElement | null>(null)

  // SoCa Evaluator flowchart definition
  const socaDiagram = `
flowchart LR
    subgraph Input
        A[/"Submission + Criteria"/]
    end

    subgraph Phase1["Phase 1 - Parallel"]
        B["Submission Evaluator<br/><small>Analyzes document</small>"]
        C["Criteria Evaluator<br/><small>Parses rubrics</small>"]
        D["Next Steps Agent<br/><small>Identifies improvements</small>"]
    end

    subgraph Phase2["Phase 2"]
        E["Scoring Agent<br/><small>Scores each criterion</small>"]
    end

    subgraph Phase3["Phase 3"]
        F["Summarizer Agent<br/><small>Creates summary</small>"]
    end

    subgraph Phase4["Phase 4 - Validation"]
        G["Sanity Check<br/><small>Validates output</small>"]
    end

    subgraph Output
        H[/"Evaluation Result"/]
    end

    A --> B
    A --> C
    A --> D
    B --> E
    C --> E
    D --> E
    E --> F
    F --> G
    G --> H

    classDef inputOutput fill:#f8f9fa,stroke:#6b7280,stroke-width:2px
    classDef parallel fill:#fef2f5,stroke:#AE0A46,stroke-width:2px
    classDef sequential fill:#fff,stroke:#AE0A46,stroke-width:2px
    classDef validation fill:#ecfdf5,stroke:#10b981,stroke-width:2px

    class A,H inputOutput
    class B,C,D parallel
    class E,F sequential
    class G validation
`

  // Criteria Generator flowchart definition
  const criteriaDiagram = `
flowchart LR
    subgraph Input
        A[/"Source Document"/]
    end

    subgraph Processing["AI Processing"]
        B["Criteria Generator<br/><small>Extracts evaluation criteria</small>"]
    end

    subgraph Output
        C[/"Generated Criteria Set"/]
    end

    A --> B
    B --> C

    classDef inputOutput fill:#f8f9fa,stroke:#6b7280,stroke-width:2px
    classDef processing fill:#f5f3ff,stroke:#3E332D,stroke-width:2px

    class A,C inputOutput
    class B processing
`

  async function renderDiagram(container: HTMLElement | null, diagram: string, id: string) {
    if (!container) return

    try {
      // Clear previous content
      container.innerHTML = ''

      // Render the diagram
      const { svg } = await mermaid.render(id, diagram)
      container.innerHTML = svg

      // Style the SVG to fit the container
      const svgElement = container.querySelector('svg')
      if (svgElement) {
        svgElement.style.maxWidth = '100%'
        svgElement.style.height = 'auto'
        svgElement.style.display = 'block'
        svgElement.style.margin = '0 auto'
      }
    } catch (error) {
      console.error('Failed to render mermaid diagram:', error)
      container.innerHTML = '<p class="text-red-500 text-sm">Failed to render diagram</p>'
    }
  }

  onMounted(async () => {
    await nextTick()
    await renderDiagram(socaContainer.value, socaDiagram, 'soca-diagram')
    await renderDiagram(criteriaContainer.value, criteriaDiagram, 'criteria-diagram')
  })

  // Re-render when switching tabs (ensures proper display)
  watch(activeWorkflow, async () => {
    await nextTick()
    if (activeWorkflow.value === 'soca') {
      await renderDiagram(socaContainer.value, socaDiagram, 'soca-diagram-' + Date.now())
    } else {
      await renderDiagram(
        criteriaContainer.value,
        criteriaDiagram,
        'criteria-diagram-' + Date.now()
      )
    }
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

    <!-- Mermaid Diagrams -->
    <div class="p-6">
      <!-- SoCa Evaluator Diagram -->
      <div
        v-show="activeWorkflow === 'soca'"
        ref="socaContainer"
        class="min-h-[350px] flex items-center justify-center"
      />

      <!-- Criteria Generator Diagram -->
      <div
        v-show="activeWorkflow === 'criteria'"
        ref="criteriaContainer"
        class="min-h-[200px] flex items-center justify-center"
      />
    </div>

    <!-- Legend -->
    <div class="px-6 py-3 bg-gray-50 border-t border-gray-100">
      <div class="flex flex-wrap items-center gap-4 text-xs text-taupe">
        <div class="flex items-center gap-1.5">
          <div class="w-3 h-3 rounded border-2 border-gray-400 bg-gray-50" />
          <span>Input/Output</span>
        </div>
        <div class="flex items-center gap-1.5">
          <div class="w-3 h-3 rounded border-2 border-shiraz bg-red-50" />
          <span>Parallel Agent</span>
        </div>
        <div class="flex items-center gap-1.5">
          <div class="w-3 h-3 rounded border-2 border-shiraz bg-white" />
          <span>Sequential Agent</span>
        </div>
        <div class="flex items-center gap-1.5">
          <div class="w-3 h-3 rounded border-2 border-green-500 bg-green-50" />
          <span>Validation</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
  /* Mermaid diagram styling */
  .mermaid {
    font-family: Inter, system-ui, sans-serif;
  }

  /* Subgraph styling */
  :deep(.cluster rect) {
    fill: #fafafa !important;
    stroke: #e5e7eb !important;
    rx: 8px !important;
    ry: 8px !important;
  }

  :deep(.cluster text) {
    fill: #3e332d !important;
    font-weight: 600 !important;
  }

  /* Edge styling */
  :deep(.flowchart-link) {
    stroke: #ae0a46 !important;
    stroke-width: 2px !important;
  }

  :deep(.marker) {
    fill: #ae0a46 !important;
    stroke: #ae0a46 !important;
  }

  /* Node text styling */
  :deep(.nodeLabel) {
    color: #222222 !important;
  }

  :deep(.nodeLabel small) {
    color: #6b7280 !important;
    font-size: 10px !important;
  }
</style>
