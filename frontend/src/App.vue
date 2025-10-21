<script setup lang="ts">
import { RouterView } from 'vue-router';
</script>

<template>
  <main class="flex-grow flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-slate-100 via-blue-100 to-slate-300">
    <RouterView />
  </main>
</template>

<style>
  .min-h-screen {
    min-height: 100vh;
  }
</style>