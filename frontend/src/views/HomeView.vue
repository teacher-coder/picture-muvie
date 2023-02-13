<template>
  <div class="my-6 mx-7 h-[70vh] flex flex-col w-full space-y-5">
    <form class="flex flex-col space-y-3" @submit.prevent="sendSongData">
      <div class="text-xl font-bold">가사 찾기</div>
      <div class="flex flex-col">
        <label for="song" class="text-lg">노래 제목</label>
        <input
          name="song"
          type="text"
          v-model="title"
          class="border-2 border-solid"
        />
      </div>
      <div class="flex flex-col">
        <label for="artist" class="text-lg">가수 이름</label>
        <input
          name="artist"
          type="text"
          v-model="artist"
          class="border-2 border-solid"
        />
      </div>
      <button class="bg-rose-600 text-white font-bold py-1 px-4 rounded-md">
        검색
      </button>
    </form>
    <form class="flex flex-col space-y-3" @submit.prevent="sendLyricsData">
      <label for="split" class="text-xl font-bold">가사 구간 나누기</label>
      <textarea
        name="split"
        type="text"
        v-model="lyrics_text"
        rows="8"
        class="p-2.5 w-full text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
      />
      <div class="text-right text-lg">
        학급 인원 : {{ lyrics_list.length }}명
      </div>
      <button class="bg-rose-600 text-white font-bold py-1 px-4 rounded-md">
        다운로드
      </button>
    </form>
  </div>
</template>

<script setup>
import api from '@/api/modules/lyrics'
import { downloadFile } from '@/utils'
import { computed, ref } from 'vue'

const title = ref('')
const artist = ref('')
const lyrics_text = ref('')
const lyrics_list = computed(() =>
  lyrics_text.value.split('\n').filter((n) => n)
)

async function sendSongData() {
  const lyrics = await api.getLyrics({
    params: { title: title.value, artist: artist.value },
  })
  lyrics_text.value = lyrics['lyrics']
}

async function sendLyricsData() {
  const docxFile = await api.downloadLyricsDocx({
    title: title.value,
    lyrics: lyrics_list.value,
  })
  downloadFile(docxFile, 'lyrics.docx')
}
</script>
