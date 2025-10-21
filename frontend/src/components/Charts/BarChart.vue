<script setup lang="ts">
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS, Title, Tooltip, Legend,
  BarElement, CategoryScale, LinearScale
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const props = defineProps<{ data: any }>()

const options = {
  responsive: true,
  plugins: {
    legend: { position: 'bottom' as const },
  },
}
</script>

<template>
    <Bar :data="props.data" :options="options" class="w-full h-[280px]" />
</template>
