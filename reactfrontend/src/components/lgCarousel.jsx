//Based on lightGallery, which is built to support mixed media galleries/sliedshows by default
import React, { useState } from "react";
import LightGallery from'lightgallery/react';
import lgvideo from "https://cdn.jsdelivr.net/npm/lg-video@1.4.0/dist/lg-video.min.js"
//styles
import  'lightgallery/css/lightgallery.css';

function LGCarousel({items}){
    //use items to generate an array of html elements
    //const [itemElements, setItemElements] = useState();
    return (
        <LightGallery 
            height={'100%'}
            slideDelay={400}
            closable= {false}
            plugins={[lgvideo]}
            dynamic={true} //allows galley to take array of items
            //Assuming items has an "src" property
            dynamicEl={items}
            >
        </LightGallery>
    )
}