<template>
  <nav class="flex flex-wrap items-center justify-between py-6">
    <div class="mr-6 flex items-center">
      <IconMovie />
      <span class="ml-6 text-xl font-semibold tracking-tight"
        >그림 뮤비 제작</span
      >
    </div>

    <div class="block items-center">
      <a
        href="https://extreme-pipe-53e.notion.site/PicMuvie-fca423162623449197924c80b68f942d"
        target="_blank"
        class="mr-4 mt-0 inline-block hover:text-red-500"
      >
        About Us
      </a>
      <a
        href="https://github.com/teacher-coder/picture-muvie"
        target="_blank"
        class="mt-0 inline-block hover:text-red-500"
      >
        Github
      </a>
    </div>
  </nav>
</template>

<script setup>
import IconMovie from '@/icons/IconMovie.vue'
</script>
