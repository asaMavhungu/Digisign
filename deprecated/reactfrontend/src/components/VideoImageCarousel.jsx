import React, { useState, useEffect, useRef } from 'react';
import Slider from 'react-slick';
import ReactPlayer from 'react-player';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

const VideoImageCarousel = ({ items }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const sliderRef = useRef(null);

  useEffect(() => {
    const interval = setInterval(() => {
      sliderRef.current.slickNext();
    }, 5000); // Change slides every 5 seconds (adjust as needed)

    return () => clearInterval(interval);
  }, []);

  const handleVideoEnded = () => {
    sliderRef.current.slickNext();
  };

  const settings = {
    dots: false,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    afterChange: (index) => setCurrentIndex(index),
  };

  const renderMedia = (item) => {
    if (item.type === 'image') {
      return <img src={item.src} alt={item.alt} />;
    } else if (item.type === 'video') {
      return (
        <ReactPlayer
          url={item.src}
          width="100%"
          height="100%"
          playing={currentIndex === items.indexOf(item)}
          controls
          onEnded={handleVideoEnded}
        />
      );
    }
    return null;
  };

  return (
    <div>
      <Slider {...settings} ref={sliderRef}>
        {items.map((item, index) => (
          <div key={index}>{renderMedia(item)}</div>
        ))}
      </Slider>
    </div>
  );
};

export default VideoImageCarousel;
