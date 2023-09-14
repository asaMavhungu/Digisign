<!-- Carousel.vue -->
<template>
	<div class="carousel-container">
	  <div class="carousel-slide" :style="`transform: translateX(-${currentIndex * 100}%)`">
		<!-- Add your divs with images and videos here -->
		<div v-for="(item, index) in items" :key="index" class="carousel-item">
		  <!-- Check the item type and render accordingly -->
		  <template v-if="item.type === 'image'">
			<img :src="item.src" alt="Carousel Image" class="carousel-image"/>
		  </template>
		  <template v-else-if="item.type === 'video'">
			<video :src="item.src" controls></video>
		  </template>
		</div>
	  </div>
  
	  <!-- Navigation Buttons -->
	  <button @click="prevSlide" class="carousel-button prev-button">Previous</button>
	  <button @click="nextSlide" class="carousel-button next-button">Next</button>
  
	  <!-- Indicators -->
	  <div v-for="(item, index) in items" :key="index" @click="goToSlide(index)" :class="{ 'active': currentIndex === index }" class="carousel-indicator"></div>
	</div>
  </template>
  
  
  <script>
  export default {
	data() {
	  return {
		currentIndex: 0,
		items: [
		  // Define your images and videos here
		  { type: 'image', src: 'https://rare-gallery.com/thumbnail/1375167-luffy-sun-god-nika-gear-5-one-piece-4k-pc-wallpaper.jpg' },
		  { type: 'image', src: 'https://www.dexerto.com/cdn-cgi/image/width=3840,quality=75,format=auto/https://editors.dexerto.com/wp-content/uploads/2023/08/13/one-piece-gear-5.jpeg' },
		  //{ type: 'video', src: 'path-to-video-1.mp4' },
		  // Add more items as needed
		  // Add more items as needed
		],
		autoplayInterval: null, // Store the autoplay interval ID
		autoplayDelay: 5000, // Autoplay delay in milliseconds (5 seconds)
	  };
	},
	methods: {
	  prevSlide() {
		// Move to the previous slide
		this.currentIndex = (this.currentIndex - 1 + this.items.length) % this.items.length;
	  },
	  nextSlide() {
		// Move to the next slide
		this.currentIndex = (this.currentIndex + 1) % this.items.length;
	  },
	  goToSlide(index) {
		// Go to the selected slide
		this.currentIndex = index;
	  },
	  startAutoplay() {
      // Start autoplay when the component is mounted or when the mouse leaves the carousel area
      this.autoplayInterval = setInterval(this.nextSlide, this.autoplayDelay);
    },
    stopAutoplay() {
      // Stop autoplay when the mouse enters the carousel area
      clearInterval(this.autoplayInterval);
    },
    resetAutoplay() {
      // Reset autoplay when navigating manually
      clearInterval(this.autoplayInterval);
      this.startAutoplay();
    },
  },
  mounted() {
    // Start autoplay when the component is mounted
    this.startAutoplay();
	},
  };
  </script>
  
  <style scoped>
  /* Add CSS styles for your carousel here */
  .carousel-container {
	overflow: hidden;
	width: 100%;
	position: relative;
  }
  
  .carousel-slide {
	display: flex;
	transition: transform 0.5s ease-in-out;
  }
  
  .carousel-item {
	flex-shrink: 0;
	width: 100%;
  }
  
  .carousel-image {
	width: 100%; /* Make the image width 100% of the parent container */
	height: 100vh; /* Set the image height to 100% of the viewport height */
	object-fit: cover; /* Ensure the image covers the entire area */
  }
  
  .carousel-video {
	width: 100%;
	height: 100vh;
	object-fit: cover;
  }
  </style>