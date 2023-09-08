
<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>


<!-- App.vue -->
<template>
  <div id="app">
    <Slideshow :slides="slides"></Slideshow>
  </div>
</template>

<script>
import Slideshow from "./components/Slideshow.vue";
import ImageSlide from "./components/ImageSlide.vue";

export default {
  components: {
    Slideshow,
    ImageSlide,
  },
  data() {
    return {
      slides: [
        {
          component: "ImageSlide",
          data: {
            imageUrl: "https://rare-gallery.com/thumbnail/1375167-luffy-sun-god-nika-gear-5-one-piece-4k-pc-wallpaper.jpg",
          },
        },
        {
          component: "ImageSlide",
          data: {
            imageUrl: "https://www.dexerto.com/cdn-cgi/image/width=3840,quality=75,format=auto/https://editors.dexerto.com/wp-content/uploads/2023/08/13/one-piece-gear-5.jpeg",
          },
        },
        // Add more slides as needed
      ],
    };
  },
};
</script>

