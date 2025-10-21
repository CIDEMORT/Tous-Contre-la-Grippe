<script setup lang="ts">
import { ref } from 'vue'
import Widget from '@/components/Widget.vue'
import DialogWidget from '@/components/DialogWidget.vue'

// Données de test
const widgetCategories = [
    {
        title: 'Données générales',
        widgets: [
            { label: 'Population' },
            { label: 'Espérance de vie' },
            { label: 'Taux de natalité' },
            { label: 'Taux de mortalité' },
        ],
    },
    {
        title: 'Santé publique',
        widgets: [
            { label: 'Vaccinations' },
            { label: 'Accès aux soins' },
            { label: 'Taux d’obésité' },
            { label: 'Activité physique' },
        ],
    },
    {
        title: 'Environnement et santé',
        widgets: [
            { label: 'Qualité de l’air' },
            { label: 'Pollution de l’eau' },
            { label: 'Gestion des déchets' },
            { label: 'Espaces verts' },
        ],
    }
]

const showDialog = ref<boolean>(false)
const selectedWidget = ref<{ label: string } | null>(null)

function openWidget(widget: { label: string }) {
    selectedWidget.value = widget
    showDialog.value = true
}
</script>

<template>
    <section class="min-h-screen bg-gradient-to-br flex flex-col items-center py-16 px-6 w-full">
        <header class="text-center max-w-2xl mb-16">
            <h1 class="text-4xl font-extrabold text-slate-800 mb-4">
                Statistiques de santé publiques 🇫🇷
            </h1>
            <p class="text-slate-600 text-lg leading-relaxed">
                Données officielles issues des ministères et agences gouvernementales.  
                Explorez les indicateurs clés de la santé publique en France.
            </p>
        </header>

        <div
            v-for="(category, index) in widgetCategories"
            :key="index"
            class="w-full max-w-5xl flex flex-col items-center mb-14"
            >
            <h2 class="text-2xl font-semibold text-slate-700 mb-2">{{ category.title }}</h2>
            <Divider class="w-1/3 mb-6" />
            <div class="flex flex-wrap justify-center gap-6">
                <Widget
                v-for="(widget, wIndex) in category.widgets"
                :key="wIndex"
                :label="widget.label"
                @click="openWidget(widget)"
                />
            </div>
        </div>

        <DialogWidget
            :showDialog="showDialog"
            :selectedWidget="selectedWidget"
            @update:showDialog="showDialog = $event"
        />
    </section>
</template>
