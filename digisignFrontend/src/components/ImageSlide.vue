<!-- ImageSlide.vue -->
<template>
  <div class="image-slide">
    <p>slideurl is {{ data.imageUrl }}</p>
    <!-- Access imageUrl from data object -->
    <img :src="data.imageUrl" alt="Image Slide">
  </div>
</template>

<script>
export default {
  props: {
    data: Object, // Pass the data object as a prop
  },
};
</script>

<style scoped>
/* Add CSS styling for image slides here */
</style>
