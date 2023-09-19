//mounts a slide containingweatheer band news widgets
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