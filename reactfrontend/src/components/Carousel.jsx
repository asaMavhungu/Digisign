import React, { useState, useEffect } from 'react';
import './Carousel.css'; // Import the CSS file

function Carousel({ items }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [autoplayInterval, setAutoplayInterval] = useState(null);
  const [responseData, setResponseData] = useState(null);
  const autoplayDelay = 5000; // 5 seconds

  useEffect(() => {
    // Start autoplay when the component is mounted
    startAutoplay();

    // Clear the interval when the component unmounts
    return () => clearInterval(autoplayInterval);
  }, []);

  useEffect(() => {
    // Reset the autoplay interval when currentIndex changes
    resetAutoplay();
  }, [currentIndex]);

  const startAutoplay = () => {
    // Start autoplay when the component is mounted
    const intervalId = setInterval(nextSlide, autoplayDelay);
    setAutoplayInterval(intervalId);
  };

  const resetAutoplay = () => {
    // Reset autoplay when navigating manually
    clearInterval(autoplayInterval);
    startAutoplay();
  };

  const nextSlide = () => {
    // Move to the next slide
    setCurrentIndex((prevIndex) => (prevIndex + 1) % items.length);
  };

  const prevSlide = () => {
    // Move to the previous slide
    setCurrentIndex((prevIndex) => (prevIndex - 1 + items.length) % items.length);
  };

  const goToSlide = (index) => {
    // Go to the selected slide
    setCurrentIndex(index);
  };

  const handleGetDataClick = () => {
    // Send a GET request to your API endpoint
    fetch('/api/devices') // Replace with the actual endpoint
      .then((response) => response.json())
      .then((data) => {
        // Process the response data and update state
        setResponseData(data);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };

  return (
    <div className="carousel-container">

      <button id="getDataButton" onClick={handleGetDataClick}>
        Get Data from API
      </button>
      <div id="responseData">
        {responseData ? (
          <pre>{JSON.stringify(responseData, null, 2)}</pre>
        ) : (
          'No data available'
        )}
      </div>

      <div className="carousel-slide" style={{ transform: `translateX(-${currentIndex * 100}%)` }}>
        {items.map((item, index) => (
          <div key={index} className="carousel-item">
            {item.type === 'image' && <img src={item.src} alt="Carousel Image" className="carousel-image" />}
            {item.type === 'video' && (
              <video src={item.src} controls className="carousel-video"></video>
            )}
          </div>
        ))}
      </div>

      <button onClick={prevSlide} className="carousel-button prev-button">
        Previous
      </button>
      <button onClick={nextSlide} className="carousel-button next-button">
        Next
      </button>

      <div className="carousel-indicators">
        {items.map((item, index) => (
          <div
            key={index}
            onClick={() => goToSlide(index)}
            className={`carousel-indicator ${currentIndex === index ? 'active' : ''}`}
          ></div>
        ))}
      </div>
    </div>
  );
}

export default Carousel;
