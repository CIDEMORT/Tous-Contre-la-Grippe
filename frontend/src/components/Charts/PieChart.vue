<script setup lang="ts">
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, ArcElement)

const props = defineProps<{ data: any }>()

const options = {
  responsive: true,
  plugins: {
    legend: { position: 'bottom' as const },
  },
}
</script>

<template>
  <Pie :data="props.data" :options="options" class="max-h-96"/>
</template>
