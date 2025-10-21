<script setup lang="ts">
const props = defineProps<{ label: string, filters: string[], title: string }>()

const getBgColor = () => {
    switch (props.title) {
        case 'géographie':
            return '#A7C7E7'
        case 'Espérance de vie':
            return '#B5EAD7'
        case 'Taux de natalité':
            return '#FFDAC1'
        case 'Taux de mortalité':
            return '#FFB7B2'
        case 'Vaccinations':
            return '#E2F0CB'
        case 'Accès aux soins':
            return '#C7CEEA'
        default:
            return '#F0F0F0'
    }
}
</script>

<template>
    <div
        class="w-full cursor-pointer select-none rounded-xl shadow-md px-8 py-6 text-center text-gray-700 font-semibold transition-all duration-300 hover:scale-105 hover:shadow-lg hover:brightness-105"
        :style="{ backgroundColor: getBgColor() }"
        @click="$emit('click')"
    >
        {{ props.label }}
    </div>
</template>
