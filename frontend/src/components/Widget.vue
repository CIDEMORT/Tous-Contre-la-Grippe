<script setup lang="ts">
import { ref, computed } from 'vue'

const colors = ['#A7C7E7', '#B5EAD7', '#FFDAC1', '#FFB7B2', '#E2F0CB', '#C7CEEA']
const randomColor = ref(colors[Math.floor(Math.random() * colors.length)])

const props = defineProps<{ label: string }>()

const bgStyle = computed(() => ({
  backgroundColor: randomColor.value,
}))
</script>

<template>
    <div
        class="cursor-pointer select-none rounded-xl shadow-md px-8 py-6 text-center text-gray-700 font-semibold transition-all duration-300 hover:scale-105 hover:shadow-lg hover:brightness-105"
        :style="bgStyle"
        @click="$emit('click')"
    >
        {{ props.label }}
    </div>
</template>
