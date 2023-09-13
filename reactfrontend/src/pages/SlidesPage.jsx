import React from 'react'
import './SlidesPage.css'
import Carousel from '../components/Carousel'

function SlidesPage() {
  const items = [
    { type: 'image', src: 'https://www.dexerto.com/cdn-cgi/image/width=3840,quality=75,format=auto/https://editors.dexerto.com/wp-content/uploads/2023/08/13/one-piece-gear-5.jpeg' },
    { type: 'image', src: 'https://rare-gallery.com/thumbnail/1375167-luffy-sun-god-nika-gear-5-one-piece-4k-pc-wallpaper.jpg' },
    { type: 'image', src: 'https://images.unsplash.com/photo-1481349518771-20055b2a7b24?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8cmFuZG9tfGVufDB8fDB8fHww&w=1000&q=80'},
    // Add more items as needed
  ];

  return (
    <div className="SlidesPage">
      <h1>React Carousel</h1>
      <Carousel items={items} />
    </div>
  );
}

export default SlidesPage
