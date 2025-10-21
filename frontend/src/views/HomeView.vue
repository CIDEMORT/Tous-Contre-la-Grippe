<script setup lang="ts">
import { ref } from 'vue'
import Widget from '@/components/Widget.vue'
import DialogWidget from '@/components/DialogWidget.vue'

const widgetCategories = [
  {
    title: 'Géographie',
    widgets: [
      {
        label: 'Évolution actes de vaccination contre la grippe de 2021 à 2024 par région',
        filters: ['year', 'region'],
      },
      {
        label: 'Accesibilité des centres de vaccination (pharmacies uniquement) selon la population',
        filters: [],
      },
      {
        label: 'Evolution des actes par age de 2021 à 2024 selon les régions',
        filters: [],
      },
      {
        label: 'Evolution des doses par age de 2021 à 2024 selon les régions',
        filters: [],
      },
      {
        label: "Repartition du lieu de vaccination selon la tranche d'age",
        filters: [],
      }
    ],
  },
  {
    title: 'Saisonnalité',
    widgets: [
        {
            label: 'Analyse de la saisonnalité - Corrélation température/grippe',
            filters: [],
        },
        {
            label: 'Repartition du taux de grippes par saisonnalité 2011 - 2025',
            filters: [],
        }
    ],
  },
  {
    title: 'Logistique',
    widgets: [
        {
            label: 'Actes/Doses de vaccination par région',
            filters: ['year', 'region'],
        },
        {
            label: 'Nombre de pharmacie sur une période/campagne de vaccination',
            filters: ['year', 'region'],
        }
    ],
  },
]

const showDialog = ref<boolean>(false)
const selectedWidget = ref<{
  label: string
  filters?: string[]
  title?: string
} | null>(null)

function openWidget(widget: { label: string; filters?: string[] }, categoryTitle: string) {
  selectedWidget.value = {
    ...widget,
    title: categoryTitle.toLowerCase(),
  }
  showDialog.value = true
}
</script>

<template>
  <section
    class="min-h-screen bg-gradient-to-br flex flex-col items-center py-16 px-6 w-full"
  >
    <header class="text-center max-w-2xl mb-16">
      <h1 class="text-4xl font-extrabold text-slate-800 mb-4">
        Statistiques de santé publiques 🇫🇷
      </h1>
      <p class="text-slate-600 text-lg leading-relaxed">
        Données officielles issues des ministères et agences gouvernementales.  
        Explorez les indicateurs clés de la santé publique en France.
      </p>
    </header>

    <!-- 🗂️ Catégories -->
    <div
      v-for="(category, index) in widgetCategories"
      :key="index"
      class="w-full max-w-5xl flex flex-col items-center mb-14"
    >
      <h2 class="text-2xl font-semibold text-slate-700 mb-2">{{ category.title }}</h2>
      <Divider class="w-1/3 mb-6" />

      <div class="flex flex-col flex-wrap justify-center gap-6 w-full">
        <Widget
          v-for="(widget, wIndex) in category.widgets"
          :key="wIndex"
          :label="widget.label"
          :filters="widget.filters"
          :title="category.title.toLowerCase()"
          @click="openWidget(widget, category.title)"
        />
      </div>
    </div>

    <!-- 💬 Dialog -->
    <DialogWidget
      :showDialog="showDialog"
      :selectedWidget="selectedWidget"
      @update:showDialog="showDialog = $event"
    />
  </section>
</template>
