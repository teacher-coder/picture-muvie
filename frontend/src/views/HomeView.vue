<template>
  <div class="mb-10 mx-7 h-[70vh] flex flex-col w-full space-y-5">
    <form class="flex flex-col space-y-3" @submit.prevent="sendSongData">
      <div class="text-xl font-bold">가사 찾기</div>
      <div class="flex flex-col">
        <label for="song" class="text-lg">노래 제목</label>
        <input
          name="song"
          type="text"
          v-model="songName"
          class="border-2 border-solid"
        />
      </div>
      <div class="flex flex-col">
        <label for="artist" class="text-lg">가수 이름</label>
        <input
          name="artist"
          type="text"
          v-model="artistName"
          class="border-2 border-solid"
        />
      </div>
      <button
        class="bg-rose-600 text-white font-bold py-1 rounded-md hover:bg-rose-800"
      >
        검색
      </button>
    </form>
    <div class="flex flex-col space-y-3">
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
      <ButtonDropDown name="다운로드" :items="items" />
    </div>
  </div>
</template>

<script setup>
import api from '@/api/modules/lyrics'
import ButtonDropDown from '@/components/ButtonDropDown.vue'
import { downloadFile } from '@/utils'
import { computed, ref } from 'vue'

const songName = ref('')
const artistName = ref('')
const lyrics_text = ref('')
const lyrics_list = computed(() =>
  lyrics_text.value.split('\n').filter((n) => n)
)
const items = [
  {
    name: 'Hwp',
    onClicked: () => downloadLyrics('.hwp'),
  },
  {
    name: 'Docx',
    onClicked: () => downloadLyrics('.docx'),
  },
]

async function sendSongData() {
  const lyrics = await api.getLyrics({
    params: { search: `${songName.value} ${artistName.value}` },
  })
  lyrics_text.value = lyrics['lyrics']
}

async function downloadLyrics(ext) {
  const docxFile = await api.downloadLyricsDocx({
    title: songName.value,
    lyrics: lyrics_list.value,
  })
  const fileName = songName.value || 'lyrics'
  downloadFile(docxFile, fileName + ext)
}
</script>
