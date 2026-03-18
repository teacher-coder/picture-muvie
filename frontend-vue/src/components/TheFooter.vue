<template>
  <footer class="bg-white">
    <div class="mx-auto overflow-hidden py-4 px-4 sm:px-6 lg:px-8">
      <nav
        class="-mx-5 -my-2 flex flex-wrap justify-center"
        aria-label="Footer"
      >
        <div v-for="item in navigation.main" :key="item.name" class="px-5 py-2">
          <a
            :href="item.href"
            target="_blank"
            class="text-md text-base text-gray-500 hover:text-gray-900"
            >{{ item.name }}</a
          >
        </div>
      </nav>
    </div>
  </footer>
</template>

<script setup>
const navigation = {
  main: [
    {
      name: 'About Us',
      href: 'https://extreme-pipe-53e.notion.site/PicMuvie-fca423162623449197924c80b68f942d',
    },
    { name: 'Github', href: 'https://github.com/teacher-coder/picture-muvie' },
  ],
}
</script>
