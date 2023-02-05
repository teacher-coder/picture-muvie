<template>
  <div class="my-6 mx-16 h-[70vh]">
    <Form class="flex flex-col">
      <label for="lyrics" class="text-xl font-bold mb-3">가사 찾기</label>
      <div>
        <Field name="lyrics" type="text" class="border-2 border-solid" />
        <button
          class="bg-rose-600 text-white font-bold py-1 px-4 ml-4 rounded-md"
        >
          검색
        </button>
      </div>
    </Form>
  </div>
</template>

<script setup>
import { Form, Field } from 'vee-validate'
</script>
