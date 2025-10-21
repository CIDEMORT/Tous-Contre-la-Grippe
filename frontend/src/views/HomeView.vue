<script setup lang="ts">
import { ref } from 'vue'
import Widget from '@/components/Widget.vue'
import DialogWidget from '@/components/DialogWidget.vue'

// 🧠 Données widgets
const widgetCategories = [
  {
    title: 'Géographie',
    widgets: [
      {
        label: 'Évolution actes de vaccination contre la grippe de 2021 à 2024 par région',
        filters: ['year', 'region'],
      },
    ],
  },
  {
    title: 'Saisonalité',
    widgets: [],
  },
  {
    title: 'Logistique',
    widgets: [],
  },
]

// ⚙️ États
const showDialog = ref<boolean>(false)
const selectedWidget = ref<{
  label: string
  filters?: string[]
  title?: string
} | null>(null)

// 🔘 Ouvrir un widget
function openWidget(widget: { label: string; filters?: string[] }, categoryTitle: string) {
  selectedWidget.value = {
    ...widget,
    title: categoryTitle.toLowerCase(), // on ajoute la catégorie au widget sélectionné
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
