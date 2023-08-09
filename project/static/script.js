document.addEventListener("DOMContentLoaded", function() {
  var slideInterval = 3000; // Change slide every 3 seconds

  var carousel = new bootstrap.Carousel(document.getElementById('carouselExample'), {
    interval: slideInterval,
    pause: "hover",
    // Add the 'carousel-fade' class to enable the crossfade effect
    wrap: true // Prevent wrapping at the end of slides
  });
});
