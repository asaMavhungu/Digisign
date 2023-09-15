import React from "react";
import {Swiper, SwiperSlide, Autoplay} from 'https://cdn.jsdelivr.net/npm/swiper@10/swiper-bundle.min.mjs'
import  ReactPlayer from 'react-player'
import { useState } from "react/cjs/react.production.min";

function SwiperCarousel({items}) {
    
    return (
        <Swiper
            autoplay={{
                // default delay
                "delay":4000
            }}>
            <SwiperSlide>
                {items.map(item,index)=>{
                    <div key={index} className="carousel-item">
                        {item.type === 'image' && <img src={item.src} alt="Carousel Image" className="carousel-image" />}
                        {item.type === 'video' && 
                            <ReactPlayer>
                                
                            </ReactPlayer>}
                    </div>
                }}
            </SwiperSlide>
        </Swiper>
    )
}
export default SwiperCarousel