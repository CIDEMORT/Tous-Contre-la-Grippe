<script lang="ts" setup>
import { ref, computed, watch } from 'vue'
import API from '@/services/API'

// 📊 Import des graphiques
import BarChart from '@/components/Charts/BarChart.vue'
import LineChart from '@/components/Charts/LineChart.vue'
import PieChart from '@/components/Charts/PieChart.vue'

// 🧩 PrimeVue
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

/* -------------------------------
🧠 États de données
---------------------------------*/
const loading = ref(false)
const apiData = ref<any | null>(null)

/* -------------------------------
🎚️ Filtres (dynamiques)
---------------------------------*/
const availableYears = ref([
  { label: '2021', value: '2021' },
  { label: '2022', value: '2022' },
  { label: '2023', value: '2023' },
  { label: '2024', value: '2024' },
])
const selectedYears = ref(['2021', '2022', '2023', '2024'])

const availableRegions = ref<{ label: string; value: string }[]>([])
const selectedRegions = ref<string[]>([])

/* -------------------------------
🧩 Type de graphique par défaut
---------------------------------*/
const chartMap: Record<string, any> = {
  'Évolution actes de vaccination contre la grippe de 2021 à 2024 par région': BarChart,
}

/* -------------------------------
🎨 Choix du graphique
---------------------------------*/
const currentChartComponent = computed(() => {
  if (!props.selectedWidget) return null
  return chartMap[props.selectedWidget.label] || BarChart
})

/* -------------------------------
📊 Données filtrées pour Chart.js
---------------------------------*/
const chartData = computed(() => {
  if (!apiData.value) return null
  const chartjsData = apiData.value.chartjs.data

  // 1️⃣ Filtrage par années
  let filteredDatasets = chartjsData.datasets
  if (props.selectedWidget?.filters?.includes('year')) {
    filteredDatasets = filteredDatasets.filter((d: any) =>
      selectedYears.value.includes(d.label)
    )
  }

  // 2️⃣ Filtrage par régions
  let filteredLabels = chartjsData.labels
  if (props.selectedWidget?.filters?.includes('region') && selectedRegions.value.length > 0) {
    const regionIndexes = filteredLabels
      .map((label: string, idx: number) =>
        selectedRegions.value.includes(label) ? idx : -1
      )
      .filter((i: any) => i !== -1)

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

/* -------------------------------
🚀 Chargement dynamique selon le widget
---------------------------------*/
async function loadWidgetData() {
  if (!props.selectedWidget) return
  loading.value = true
  apiData.value = null

  try {
    // Exemple : gestion par titre + label
    switch (props.selectedWidget.title) {
      case 'géographie':
        apiData.value = (await API.geographie.getEvolutionActesRegion()).data

        // Initialise le filtre région
        availableRegions.value = apiData.value.chartjs.data.labels.map((label: string) => ({
          label,
          value: label,
        }))
        selectedRegions.value = availableRegions.value.map((r) => r.value)
        break

      // Tu pourras ajouter ici d'autres "titles" comme "saisonalité" ou "logistique"
    }
  } catch (err) {
    console.error('Erreur API:', err)
  } finally {
    loading.value = false
  }
}

// 🔁 Recharger à chaque changement de widget
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
    <!-- 🧩 HEADER -->
    <template #header>
      <div class="flex flex-col gap-3 w-full">
        <h2 class="text-xl font-semibold text-center text-slate-800">
          {{ props.selectedWidget?.label }}
        </h2>
      </div>
    </template>

    <!-- 📊 CONTENU -->
    <div class="flex flex-col items-center justify-center min-h-[400px] w-full">
      <div v-if="loading" class="text-gray-500 italic">Chargement...</div>

      <component
        v-else-if="currentChartComponent && chartData"
        :is="currentChartComponent"
        :data="chartData"
      />

      <p v-else class="text-gray-500 italic">Aucune donnée disponible</p>
    </div>

    <!-- 🔚 FOOTER -->
    <template #footer>
      <div class="w-full flex gap-4 justify-between pt-4 border-t border-slate-200">
        <div class="border-t border-slate-200 my-4"></div>
        <!-- 🎚️ Filtres -->
        <div class="flex flex-wrap justify-center gap-4">
          <!-- 🔹 Filtres dynamiques -->
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
