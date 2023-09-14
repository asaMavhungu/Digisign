<!-- Slideshow.vue -->
<template>
  <div class="slideshow">
		<p> data is: {{ currentSlide.data }} </p>
		// This shows that data corrently. i want it to be extracted by the component tho
    <component :is="currentSlide.component" :data="currentSlide.data"></component>
  </div>
</template>

<script>
export default {
  props: {
    slides: Array,
  },
  data() {
    return {
      currentSlideIndex: 0,
    };
  },
  computed: {
    currentSlide() {
      return this.slides[this.currentSlideIndex];
    },
  },
  methods: {
    nextSlide() {
      this.currentSlideIndex = (this.currentSlideIndex + 1) % this.slides.length;
    },
  },
  mounted() {
    setInterval(this.nextSlide, 5000); // Change slide every 5 seconds (adjust as needed)
  },
};
</script>

<style scoped>
/* Add CSS styling for the parent slideshow here */
</style>
