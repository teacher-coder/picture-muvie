<template>
  <Menu as="div" class="relative inline-block text-left">
    <MenuButton
      class="inline-flex rounded-md border border-transparent bg-secondary px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-primary focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 sm:text-sm"
    >
      {{ name }}
      <ChevronDownIcon
        class="ml-2 -mr-1 h-5 w-5 text-white"
        aria-hidden="true"
      />
    </MenuButton>

    <transition
      enter-active-class="transition duration-100 ease-out"
      enter-from-class="transform scale-95 opacity-0"
      enter-to-class="transform scale-100 opacity-100"
      leave-active-class="transition duration-75 ease-in"
      leave-from-class="transform scale-100 opacity-100"
      leave-to-class="transform scale-95 opacity-0"
    >
      <MenuItems
        class="absolute right-0 mt-2 w-28 origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
      >
        <div class="px-1 py-1">
          <MenuItem
            v-slot="{ active }"
            v-for="(item, index) in items"
            :key="index"
          >
            <button
              :class="[
                active ? 'bg-secondary text-white' : 'text-gray-900',
                'flex w-full items-center rounded-md px-2 py-2 text-sm',
              ]"
              @click="item.onClicked"
            >
              {{ item.name }}
            </button>
          </MenuItem>
        </div>
      </MenuItems>
    </transition>
  </Menu>
</template>

<script setup>
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
