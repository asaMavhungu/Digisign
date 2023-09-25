import React from 'react'
import { Splide, SplideSlide } from '@splidejs/react-splide'
import { Video } from '@splidejs/splide-extension-video';
import '@splidejs/react-splide/css';
import "@splidejs/splide-extension-video/dist/css/splide-extension-video.min.css"

function SplideCarousel({items}){
    const options = {
        autoplay: true,
        video: {
            mute: true,
            autoplay: true, //video plays when it appears
            disableOverlayUI: true,
        }   
    }
    const slideImageStyle = {
        width: "100%",
        height: "auto"
    }

    return (
    <Splide options ={options} extensions= {Video}>
        {items.map((item, index) =>(
            <SplideTrack>
                {item.type === 'image' && 
                    <SplideSlide key={index}>
                            <img src={item.src} 
                                alt="Carousel Image" 
                                className="carousel-image"/>
                    </SplideSlide>
                }
                {item.type === 'video' &&(
                    <SplideSlide 
                        key={index} 
                        data-splide-youtube={item.src}
                        style={slideImageStyle}>
                    </SplideSlide>
                )}

            </SplideTrack>
        ))}
    </Splide>
    )
}

export default SplideCarousel