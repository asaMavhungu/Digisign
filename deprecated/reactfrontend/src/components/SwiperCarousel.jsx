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

        </Swiper>
    )
}
export default SwiperCarousel