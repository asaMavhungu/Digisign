import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import ImageSlide from './components/ImageSlide.vue' // Import your ImageSlide component

const app = createApp(App)

// Register your ImageSlide component globally
app.component('ImageSlide', ImageSlide)

app.mount('#app')
