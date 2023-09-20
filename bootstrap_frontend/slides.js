// Function to create custom styled carousel indicators (buttons)
function createCarouselIndicators(slides) {
    const carouselIndicators = document.getElementById('carouselIndicators');

    slides.forEach((slide, index) => {
        const indicatorButton = document.createElement('li');
        indicatorButton.classList.add('indicator-button'); // Add custom styling class
        indicatorButton.setAttribute('data-bs-target', '#carousel');
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

function createNewsWeatherSlide(){
    const RSS_URL = "https://widgets.sociablekit.com/rss-feed/widget.js";
    const weatherURL = "https://forecast7.com/en/n33d9218d42/cape-town/";

    const slideContent = `<div>
        <div class="weathr-container" style="">
            <a class="weatherwidget-io" href=${weatherURL} data-label_1="CAPE TOWN" data-label_2="WEATHER" data-icons="Climacons Animated" data-theme="original" >CAPE TOWN WEATHER</a>
        </div>

        <!--Weather Script-->
        <script>
            !function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src='https://weatherwidget.io/js/widget.min.js';fjs.parentNode.insertBefore(js,fjs);}}(document,'script','weatherwidget-io-js');
        </script>

        <div class="newsContainer">
            <div class='sk-ww-rss-feed' data-embed-id='196641'></div><script src=${RSS_URL} async defer></script>
        </div>
    </div>`

    const carouselItem = document.createElement('div');
    carouselItem.classList.add('carousel-item');

    const carouselInner = document.getElementById('carouselInner');

    carouselItem.innerHTML = slideContent;
    carouselInner.appendChild(carouselItem);
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