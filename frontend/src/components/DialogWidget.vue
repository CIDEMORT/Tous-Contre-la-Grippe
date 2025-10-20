<script lang="ts" setup>
import { ref, computed } from 'vue'

// 📊 Import des graphiques
import BarChart from '@/components/Charts/BarChart.vue'
import LineChart from '@/components/Charts/LineChart.vue'
import PieChart from '@/components/Charts/PieChart.vue'

// 🧩 PrimeVue
import MultiSelect from 'primevue/multiselect'

const props = defineProps<{
  showDialog: boolean
  selectedWidget: { label: string } | null
}>()

const emit = defineEmits<(
  e: 'update:showDialog', value: boolean
) => void>()

const handleHide = () => {
  emit('update:showDialog', false)
}

/**
 * 🔎 Filtres disponibles
 */
const availableDates = ref([
  { label: '2019', value: '2019' },
  { label: '2020', value: '2020' },
  { label: '2021', value: '2021' },
  { label: '2022', value: '2022' },
  { label: '2023', value: '2023' },
  { label: '2024', value: '2024' }
])
const selectedDates = ref(['2024'])

/**
 * 1️⃣ Correspondance widget → composant graphique
 */
const chartMap: Record<string, any> = {
  'Population': BarChart,
  'Espérance de vie': LineChart,
  'Taux d’obésité': PieChart,
}

/**
 * 2️⃣ Détermination du graphique à afficher
 */
const currentChartComponent = computed(() => {
  if (!props.selectedWidget) return null
  return chartMap[props.selectedWidget.label] || BarChart
})

/**
 * 3️⃣ Données dynamiques simulées
 */
const chartData = computed(() => {
  if (!props.selectedWidget) return null

  // Filtrage factice selon les dates sélectionnées (pour l’exemple)
  const years = selectedDates.value
  const baseData = [62, 64.3, 67.5, 68].slice(0, years.length)

  switch (props.selectedWidget.label) {
    case 'Population':
      return {
        labels: years,
        datasets: [{ label: 'Millions', data: baseData, backgroundColor: '#A7C7E7' }],
      }
    case 'Espérance de vie':
      return {
        labels: ['Hommes', 'Femmes'],
        datasets: [{ label: 'Années', data: [79.5, 85.7], backgroundColor: ['#B5EAD7', '#FFDAC1'] }],
      }
    case 'Taux d’obésité':
      return {
        labels: ['Hommes', 'Femmes'],
        datasets: [{ label: '%', data: [15.2, 17.3], backgroundColor: ['#FFB7B2', '#C7CEEA'] }],
      }
    default:
      return {
        labels: ['A', 'B', 'C', 'D'],
        datasets: [{ label: 'Valeurs simulées', data: [10, 20, 15, 25], backgroundColor: '#E2F0CB' }],
      }
  }
})
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
    <!-- Header -->
    <template #header>
      <div class="flex flex-col w-full gap-3">
        <h2 class="text-xl font-semibold text-slate-800 text-center">
          {{ props.selectedWidget?.label }}
        </h2>

        <!-- 🎚️ Zone de filtres -->
        <div class="flex items-center gap-4 mt-2 justify-center">
          <div class="flex flex-col">
            <MultiSelect
              id="dateFilter"
              v-model="selectedDates"
              :options="availableDates"
              optionLabel="label"
              optionValue="value"
              placeholder="Choisir des années"
              display="chip"
              class="w-64 !bg-white"
            />
          </div>
        </div>
      </div>
    </template>

    <!-- Contenu -->
    <div class="flex items-center justify-center min-h-[350px]">
      <component
        v-if="currentChartComponent && chartData"
        :is="currentChartComponent"
        :data="chartData"
      />
      <p v-else class="text-gray-500 italic">Aucune donnée disponible</p>
    </div>

    <!-- Footer -->
    <template #footer>
      <div class="flex justify-end">
        <button
          class="px-4 py-2 rounded-md bg-slate-700 text-white hover:bg-slate-800 transition"
          @click="handleHide"
        >
          Fermer
        </button>
      </div>
    </template>
  </Dialog>
</template>
