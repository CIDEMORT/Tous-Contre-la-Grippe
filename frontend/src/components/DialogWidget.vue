<script lang="ts" setup>
import { ref, computed, watch } from 'vue'
import API from '@/services/API'

import BarChart from '@/components/Charts/BarChart.vue'
import LineChart from '@/components/Charts/LineChart.vue'
import PieChart from '@/components/Charts/PieChart.vue'

import MultiSelect from 'primevue/multiselect'

const props = defineProps<{
  showDialog: boolean
  selectedWidget: {
    label: string
    filters?: string[]
    title?: string
  } | null
}>()

const emit = defineEmits<(e: 'update:showDialog', value: boolean) => void>()
const handleHide = () => emit('update:showDialog', false)

const loading = ref(false)
const apiData = ref<any | null>(null)

const availableYears = ref([
  { label: '2021', value: '2021' },
  { label: '2022', value: '2022' },
  { label: '2023', value: '2023' },
  { label: '2024', value: '2024' },
])
const selectedYears = ref(['2021', '2022', '2023', '2024'])

const availableRegions = ref<{ label: string; value: string }[]>([])
const selectedRegions = ref<string[]>([])

const chartMap: Record<string, any> = {
  'Évolution actes de vaccination contre la grippe de 2021 à 2024 par région': BarChart,
  'Analyse de la saisonnalité - Corrélation température/grippe': LineChart,
}

const currentChartComponent = computed(() => {
  if (!props.selectedWidget) return null
  return chartMap[props.selectedWidget.label] || BarChart
})

const chartData = computed(() => {
  if (!apiData.value) return null

  const filters = props.selectedWidget?.filters?.filter(f => f && f.trim() !== '') || []
  const hasFilters = filters.length > 0
  const chartjsData = apiData.value.chartjs.data

  if (!hasFilters) {
    return {
      ...chartjsData,
      labels: [...chartjsData.labels],
      datasets: chartjsData.datasets.map((d: any) => ({ ...d, data: [...d.data] })),
    }
  }

  let filteredDatasets = chartjsData.datasets
  let filteredLabels = chartjsData.labels

  if (filters.includes('year')) {
    filteredDatasets = filteredDatasets.filter((d: any) =>
      selectedYears.value.includes(d.label)
    )
  }

  if (filters.includes('region') && selectedRegions.value.length > 0) {
    const regionIndexes = filteredLabels
      .map((label: string, idx: number) =>
        selectedRegions.value.includes(label) ? idx : -1
      )
      .filter((i: number) => i !== -1)

    filteredLabels = filteredLabels.filter((label: string) =>
      selectedRegions.value.includes(label)
    )

    filteredDatasets = filteredDatasets.map((dataset: any) => ({
      ...dataset,
      data: dataset.data.filter((_: any, idx: number) => regionIndexes.includes(idx)),
    }))
  }

  return {
    labels: filteredLabels,
    datasets: filteredDatasets,
  }
})

const getEvolutionActesRegion = async () => {
  apiData.value = (await API.geographie.getEvolutionActesRegion()).data

  availableRegions.value = apiData.value.chartjs.data.labels.map((label: string) => ({
    label,
    value: label,
  }))
  selectedRegions.value = availableRegions.value.map((r) => r.value)
}

const getDonneesMeteo = async () => {
  apiData.value = (await API.saisonnalite.getDonneesMeteo()).data

  availableRegions.value = apiData.value.chartjs.data.labels.map((label: string) => ({
    label,
    value: label,
  }))
  selectedRegions.value = availableRegions.value.map((r) => r.value)
}

async function loadWidgetData() {
  if (!props.selectedWidget) return
  loading.value = true
  apiData.value = null

  try {
    switch (props.selectedWidget.title) {
      case 'géographie':
        if (props.selectedWidget.label === 'Évolution actes de vaccination contre la grippe de 2021 à 2024 par région') {
          await getEvolutionActesRegion()
        }
        break
      case 'saisonnalité':
        if (props.selectedWidget.label === 'Analyse de la saisonnalité - Corrélation température/grippe') {
          await getDonneesMeteo()
        }
        break
      case 'logistique':
        break
      default:
        apiData.value = null
        break
    }
  } catch (err) {
    console.error('Erreur API:', err)
  } finally {
    loading.value = false
  }
}

watch(() => props.selectedWidget, loadWidgetData, { immediate: true })
</script>

<template>
  <Dialog
    :visible="props.showDialog"
    @update:visible="emit('update:showDialog', $event)"
    @hide="handleHide"
    modal
    dismissableMask
    :style="{ width: '90%' }"
    class="!bg-white"
  >
    <template #header>
      <div class="flex flex-col gap-3 w-full">
        <h2 class="text-xl font-semibold text-center text-slate-800">
          {{ props.selectedWidget?.label }}
        </h2>
      </div>
    </template>

    <div class="flex flex-col items-center justify-center min-h-[400px] w-full">
      <div v-if="loading" class="text-gray-500 italic">Chargement...</div>

      <component
        v-else-if="currentChartComponent && chartData"
        :is="currentChartComponent"
        :options="apiData?.chartjs?.options"
        :data="chartData"
      />

      <p v-else class="text-gray-500 italic">Aucune donnée disponible</p>
    </div>

    <template #footer>
      <div class="w-full flex gap-4 justify-between pt-4 border-t border-slate-200">
        <div class="border-t border-slate-200 my-4"></div>
        <div class="flex flex-wrap justify-center gap-4">
          <MultiSelect
            v-if="props.selectedWidget?.filters?.includes('year')"
            v-model="selectedYears"
            :options="availableYears"
            optionLabel="label"
            optionValue="value"
            placeholder="Choisir des années"
            display="chip"
            class="w-64 !bg-white"
          />
          <MultiSelect
            v-if="props.selectedWidget?.filters?.includes('region')"
            v-model="selectedRegions"
            :options="availableRegions"
            optionLabel="label"
            optionValue="value"
            placeholder="Filtrer par région"
            display="chip"
            class="w-80 !bg-white"
          />
        </div>
        <div class="flex justify-end items-center">
          <button
            class="px-4 py-2 rounded-md bg-slate-700 text-white hover:bg-slate-800 transition h-[2.5rem] flex items-center justify-center"
            @click="handleHide"
          >
            Fermer
          </button>
        </div>
      </div>
    </template>
  </Dialog>
</template>
