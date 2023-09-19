// Function to create custom styled carousel indicators (buttons)
function createCarouselIndicators(slides) {
    const carouselIndicators = document.getElementById('carouselIndicators');

    slides.forEach((slide, index) => {
        const indicatorButton = document.createElement('li');
        indicatorButton.classList.add('indicator-button'); // Add custom styling class
        indicatorButton.setAttribute('data-bs-target', '#carouselExampleCaptions');
        indicatorButton.setAttribute('data-bs-slide-to', index);
        indicatorButton.setAttribute('aria-label', `Slide ${index + 1}`);
        if (index === 0) {
            indicatorButton.classList.add('active');
        }
        carouselIndicators.appendChild(indicatorButton);
    });
}

// Function to create carousel items
function createCarouselItems(slides) {
    const carouselInner = document.getElementById('carouselInner');

    slides.forEach((slide, index) => {
        const carouselItem = document.createElement('div');
        carouselItem.classList.add('carousel-item');
        if (index === 0) {
            carouselItem.classList.add('active');
        }

        let slideContent;

        // For other items, include an image
        slideContent = `
            <img src="${slide.image_url}" class="d-block w-100" alt="...">
            <div class="carousel-caption d-none d-md-block">
                <h5>${slide.title}</h5>
                <p>${slide.description}</p>
            </div>
        `;

        carouselItem.innerHTML = slideContent;
        carouselInner.appendChild(carouselItem);
    });
}

// Fetch data from the API and populate the carousel
fetch('/api/slides', {
    method: 'GET',
    // Additional options like headers can be provided here
})
    .then(response => response.json())
    .then(data => {
        const slides = data; // Assuming data is an array of slide objects
        createCarouselIndicators(slides);
        createCarouselItems(slides);
    })
    .catch(error => {
        console.error('Error:', error);
    });