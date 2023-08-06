
// Wait for the DOM to load before running the JavaScript
document.addEventListener("DOMContentLoaded", function() {
	// Get references to the parent div and its children
	const slideshow = document.getElementById("slideshow");
	const slides = slideshow.getElementsByClassName("slide");

	let currentSlideIndex = 0;

	function showSlide(index) {
		// Hide all slides
		for (let i = 0; i < slides.length; i++) {
		slides[i].style.display = "none";
		}

		// Show the slide at the specified index
		slides[index].style.display = "flex";
		slides[index].style.flex = "1 100%"; // Set the flex properties
	}

	function nextSlide() {
		currentSlideIndex = (currentSlideIndex + 1) % slides.length;
		showSlide(currentSlideIndex);
	}

	function prevSlide() {
		currentSlideIndex = (currentSlideIndex -1) % slides.length;
		showSlide(currentSlideIndex);
	}

	// Start the slideshow
	setInterval(nextSlide, 3000); // Change slide every 3 seconds (adjust as needed)

	// Get a reference to the link element
	const prev = document.getElementById("Prev");
	const next = document.getElementById("Next");

	// Define the function to be executed when the link is clicked
	function handleClick(event) {
		event.preventDefault(); // Prevent the default link behavior (e.g., navigating to the href)

		// Your custom JavaScript function code here
		// For example, you can show an alert when the link is clicked
		alert("You clicked the link!");
	}

	// Add the event listener to the link
	myLink.addEventListener("click", handleClick);


});


