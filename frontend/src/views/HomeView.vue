<template>
  <div class="my-5 flex w-full flex-col space-y-5">
    <Form class="flex flex-col space-y-3" @submit="searchLyrics">
      <label for="query" class="text-xl font-bold">가사 찾기</label>
      <div class="flex flex-col">
        <Field
          name="query"
          type="text"
          v-model="query"
          class="rounded-lg border border-solid border-gray-300 bg-gray-50 p-2.5"
          :rules="isRequired"
          placeholder="노래 제목과 가수 입력 - 예시) 출발 김동률, ditto newjeans"
        />
        <ErrorMessage name="query" class="text-red-700" />
      </div>
      <button
        class="flex justify-center rounded-md bg-rose-600 py-1 font-bold text-white hover:bg-rose-800"
        :disabled="searching"
      >
        <span v-if="searching"
          ><svg
            class="h-5 w-5 animate-spin"
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
    </Form>
    <div class="flex flex-col space-y-3">
      <div class="flex justify-between">
        <label for="split" class="text-xl font-bold">가사 구간 나누기</label>
        <div class="space-x-3">
          <button
            class="rounded-md border border-solid border-gray-400 px-3 py-1 font-medium text-gray-900 hover:bg-gray-50"
            @click="increaseLyricsCompression()"
          >
            가사 압축하기
          </button>
        </div>
      </div>
      <textarea
        name="split"
        placeholder="입력된 줄의 개수는 학생 수를 나타냅니다&#10;enter키를 눌러 줄을 바꾸고 학생 수를 조정해주세요&#10;아래에 학급 인원 수를 확인하실 수 있습니다"
        type="text"
        v-model="lyrics_text"
        rows="8"
        class="w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-900 focus:border-blue-500 focus:ring-blue-500"
      />
      <div class="flex justify-between">
        <div class="text- text-lg">출처 : {{ lyrics_source }}</div>
        <div class="text-right text-lg">
          학급 인원 : {{ lyrics_list.length }}명
        </div>
      </div>
      <ButtonDropDown name="다운로드" :items="items" />
    </div>
  </div>
</template>

<script setup>
import api from '@/api/modules/lyrics'
import ButtonDropDown from '@/components/ButtonDropDown.vue'
import { compressLyrics, downloadFile } from '@/utils'
import { Form, Field, ErrorMessage } from 'vee-validate'
import { computed, ref } from 'vue'

const query = ref('')
const searching = ref(false)
const defaultOffset = 30

const lyrics_text = ref('')
const lyrics_source = ref('')
const lyrics_title = ref('')
const lyrics_artist = ref('')
const lyrics_list = computed(() =>
  lyrics_text.value.split('\n').filter((n) => n)
)
const minLineLength = computed(() => lyrics_text.value.split('\n\n').length)
function isRequired(value) {
  if (value && value.trim()) {
    return true
  }
  return '필수로 입력해야 합니다'
}

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
      params: { query: query.value },
    })
    .catch(() => {
      lyrics_text.value = '에러가 발생했습니다. 다음에 다시 시도해주세요.'
    })
  searching.value = false
  if (!response) return
  lyrics_text.value = compressLyrics(response['lyrics'], defaultOffset)
  lyrics_source.value = response['source']
  lyrics_title.value = response['title']
  lyrics_artist.value = response['artist']
}

async function downloadLyrics(ext) {
  const docxFile = await api.downloadLyricsDocx({
    title: lyrics_title.value,
    lyrics: lyrics_list.value,
  })

  const fileName = lyrics_title.value + '-' + lyrics_artist.value || 'lyrics'
  downloadFile(docxFile, fileName + ext)
}
</script>
