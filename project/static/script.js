document.addEventListener("DOMContentLoaded", function() {
  var slideInterval = 3000; // Change slide every 3 seconds

  var carousel = new bootstrap.Carousel(document.getElementById('carouselExample'), {
    interval: slideInterval,
    pause: "hover",
    // Add the 'carousel-fade' class to enable the crossfade effect
    wrap: true // Prevent wrapping at the end of slides
  });
  // TODO: Redo slideshow 
  // https://www.youtube.com/watch?v=ku_97a6Bgkg
  // https://www.youtube.com/watch?v=dam0GPOAvVI&t=3795s
});
