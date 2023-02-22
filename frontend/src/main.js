import App from '@/App.vue'
import '@/assets/main.css'
import router from '@/router'
import { createPinia } from 'pinia'
import { createApp } from 'vue'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.provide('axios', app.config.globalProperties.axios)

app.mount('#app')
