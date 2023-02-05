<template>
  <nav class="flex items-center justify-between flex-wrap p-6">
    <div class="flex items-center flex-shrink-0 mr-6">
      <IconMovie />
      <span class="font-semibold text-xl tracking-tight ml-6"
        >그림 뮤비 제작</span
      >
    </div>

    <div class="w-full block flex-grow lg:flex lg:items-center lg:w-auto">
      <div class="text-sm lg:flex-grow">
        <a class="block mt-4 lg:inline-block lg:mt-0 hover:text-red-500 mr-4">
          사용방법
        </a>
        <a class="block mt-4 lg:inline-block lg:mt-0 hover:text-red-500 mr-4">
          건의하기
        </a>
      </div>
      <div>
        <a
          href="#"
          class="inline-block text-sm px-4 py-2 leading-none border rounded text-white border-white hover:border-transparent hover:text-teal-500 hover:bg-white mt-4 lg:mt-0"
          >Download</a
        >
      </div>
    </div>
  </nav>
</template>

<script setup>
import IconMovie from '@/icons/IconMovie.vue'
</script>
