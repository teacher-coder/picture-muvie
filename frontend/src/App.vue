<template>
  <header>
    <TheHeader />
  </header>
  <main class="flex">
    <RouterView />
  </main>
  <footer>
    <TheFooter />
  </footer>
</template>

<script setup>
import TheFooter from '@/components/TheFooter.vue'
import TheHeader from '@/components/TheHeader.vue'
import { RouterView } from 'vue-router'
</script>
