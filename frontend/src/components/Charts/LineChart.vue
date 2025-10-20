<script setup lang="ts">
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS, Title, Tooltip, Legend,
  LineElement, CategoryScale, LinearScale, PointElement
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

const props = defineProps<{ data: any }>()

const options = {
  responsive: true,
  plugins: {
    legend: { position: 'bottom' as const},
  },
}
</script>

<template>
  <Line :data="props.data" :options="options" class="w-full h-[280px]" />
</template>
