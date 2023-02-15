<template>
  <div class="mb-10 mx-7 h-[70vh] flex flex-col w-full space-y-5">
    <form class="flex flex-col space-y-3" @submit.prevent="searchLyrics">
      <div class="text-xl font-bold">가사 찾기</div>
      <div class="flex flex-col">
        <label for="song" class="text-lg">노래 제목</label>
        <input
          name="song"
          type="text"
          v-model="title"
          class="border-2 border-solid"
          required
        />
      </div>
      <div class="flex flex-col">
        <label for="artist" class="text-lg">가수 이름</label>
        <input
          name="artist"
          type="text"
          v-model="artist"
          class="border-2 border-solid"
          required
        />
      </div>
      <button
        class="bg-rose-600 text-white font-bold py-1 rounded-md hover:bg-rose-800"
        :disabled="searching"
      >
        <span v-if="searching"
          ><svg
            class="h-5 w-5 flex justify-center animate-spin"
            fill="currentColor"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 512 512"
          >
            <path
              d="M126.9 142.9c62.2-62.2 162.7-62.5 225.3-1L311 183c-6.9 6.9-8.9 17.2-5.2 26.2s12.5 14.8 22.2 14.8H447.5c0 0 0 0 0 0H456c13.3 0 24-10.7 24-24V72c0-9.7-5.8-18.5-14.8-22.2s-19.3-1.7-26.2 5.2L397.4 96.6c-87.6-86.5-228.7-86.2-315.8 1C57.2 122 39.6 150.7 28.8 181.4c-5.9 16.7 2.9 34.9 19.5 40.8s34.9-2.9 40.8-19.5c7.7-21.8 20.2-42.3 37.8-59.8zM0 312v7.6 .7V440c0 9.7 5.8 18.5 14.8 22.2s19.3 1.7 26.2-5.2l41.6-41.6c87.6 86.5 228.7 86.2 315.8-1c24.4-24.4 42.1-53.1 52.9-83.7c5.9-16.7-2.9-34.9-19.5-40.8s-34.9 2.9-40.8 19.5c-7.7 21.8-20.2 42.3-37.8 59.8c-62.2 62.2-162.7 62.5-225.3 1L169 329c6.9-6.9 8.9-17.2 5.2-26.2s-12.5-14.8-22.2-14.8H32.4h-.7H24c-13.3 0-24 10.7-24 24z"
            />
          </svg>
        </span>
        <span v-else> 검색 </span>
      </button>
    </form>
    <div class="flex flex-col space-y-3">
      <div class="flex justify-between">
        <label for="split" class="text-xl font-bold">가사 구간 나누기</label>
        <div class="space-x-3">
          <button
            class="border border-solid border-gray-400 text-gray-900 font-medium px-3 py-1 rounded-md hover:bg-rose-800"
            @click="increaseLyricsCompression()"
          >
            가사 압축하기
          </button>
        </div>
      </div>
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
import { compressLyrics, downloadFile } from '@/utils'
import { computed, ref } from 'vue'

const title = ref('')
const artist = ref('')
const searching = ref(false)
const defaultOffset = 35

const lyrics_text = ref('')
const lyrics_list = computed(() =>
  lyrics_text.value.split('\n').filter((n) => n)
)
const minLineLength = computed(() => lyrics_text.value.split('\n\n').length)
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

function increaseLyricsCompression() {
  if (!lyrics_text.value) return

  let compressOffset = defaultOffset
  let curLineLength = lyrics_list.value.length
  while (curLineLength === lyrics_list.value.length) {
    if (curLineLength === minLineLength.value) break
    compressOffset += 1
    lyrics_text.value = compressLyrics(lyrics_text.value, compressOffset)
  }
}

async function searchLyrics() {
  searching.value = true
  const response = await api
    .getLyrics({
      params: { title: title.value, artist: artist.value },
    })
    .catch(() => {
      lyrics_text.value = '에러가 발생했습니다. 다음에 다시 시도해주세요.'
    })
  searching.value = false
  if (!response) return
  lyrics_text.value = compressLyrics(response['lyrics'], defaultOffset)
}

async function downloadLyrics(ext) {
  const docxFile = await api.downloadLyricsDocx({
    title: title.value,
    lyrics: lyrics_list.value,
  })

  const fileName = title.value || 'lyrics'
  downloadFile(docxFile, fileName + ext)
}
</script>
