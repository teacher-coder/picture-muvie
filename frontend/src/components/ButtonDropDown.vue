<template>
  <Menu>
    <Float
      placement="right-end"
      :offset="10"
      enter="transition duration-200 ease-out"
      enter-from="scale-95 opacity-0"
      enter-to="scale-100 opacity-100"
      leave="transition duration-150 ease-in"
      leave-from="scale-100 opacity-100"
      leave-to="scale-95 opacity-0"
      tailwindcss-origin-class
    >
      <MenuButton class="bg-rose-600 text-white font-bold py-2">
        <span class="inline-flex">
          {{ name }}
          <ChevronDownIcon
            class="ml-2 h-5 w-5 text-white -rotate-90"
            aria-hidden="true"
        /></span>
      </MenuButton>

      <MenuItems class="space-y-3 mb-3">
        <MenuItem
          v-slot="{ active }"
          v-for="(item, index) in items"
          :key="index"
        >
          <button
            :class="[
              active ? ' bg-rose-800 text-white' : 'bg-rose-600 text-white',
              'flex w-full items-center px-10 py-2 text-sm',
            ]"
            @click="item.onClicked"
          >
            {{ item.name }}
          </button>
        </MenuItem>
      </MenuItems>
    </Float>
  </Menu>
</template>

<script setup>
import { Float } from '@headlessui-float/vue'
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { ChevronDownIcon } from '@heroicons/vue/20/solid'

defineProps({
  name: String,
  items: {
    type: Array,
    required: true,
    validator: (items) => {
      const item = items[0]
      let item_name = item.name && typeof item.name === 'string'
      let item_onClicked =
        item.onClicked && typeof item.onClicked === 'function'
      return item_name && item_onClicked
    },
  },
})
</script>
