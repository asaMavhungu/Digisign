// Create and add a feed to News 24
const RSS_URL ="https://feeds.capi24.com/v1/Search/articles/news24/TopStories/rss"

async function fetchAndDisplayRSSFeed() {
    const response = await fetch(RSS_URL);
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, 'text/xml');
    const items = xmlDoc.querySelectorAll('item');

    const feedContainer = document.getElementById('feedContainer');

    items.forEach((item, index) => {
      if (index < 4) {  // Display the 4 most recent entries
        const title = item.querySelector('title').textContent;
        const img = item.querySelector('enclosure').url;
        const description = item.querySelector('description').textContent;

        const card = document.createElement('div');
        card.classList.add('col-md-3', 'mb-4');

        card.innerHTML = `
          <div class="card">
            <img src="YOUR_IMAGE_URL" class="card-img-top" alt="Card image">
            <div class="card-body">
                <img><img>
                <h5 class="card-title">${title}</h5>
                <p class="card-text">${description}</p>
            </div>
          </div>
        `;

        feedContainer.appendChild(card);
      }
    });
  }

  // Call the function to fetch and display the RSS feed
  fetchAndDisplayRSSFeed();
