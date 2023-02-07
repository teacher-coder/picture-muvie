import App from '@/App.vue'
import router from '@/router'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import '@/assets/main.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.provide('axios', app.config.globalProperties.axios)
app.mount('#app')
