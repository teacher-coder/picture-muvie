<template>
  <div class="my-6 mx-16 h-[70vh]">
    <form class="flex flex-col" @submit.prevent="searchLyrics">
      <label for="search" class="text-xl font-bold mb-3">가사 찾기</label>
      <div>
        <input
          name="search"
          type="text"
          v-model="searchTerm"
          class="border-2 border-solid"
        />
        <button
          class="bg-rose-600 text-white font-bold py-1 px-4 ml-4 rounded-md"
        >
          검색
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/api/modules/lyrics'

const searchTerm = ref('')
async function searchLyrics() {
  console.log(searchTerm.value)
  const lyrics = await api.getLyrics({ params: { search: searchTerm.value } })
  console.log(lyrics)
}
</script>
