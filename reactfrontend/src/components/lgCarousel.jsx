//Based on lightGallery, which is built to support mixed media galleries/sliedshows by default
import React, { useCallback, useState } from "react";
import LightGallery from'lightgallery/react';
import lgvideo from "https://cdn.jsdelivr.net/npm/lg-video@1.4.0/dist/lg-video.min.js"
//styles
import  'lightgallery/css/lightgallery.css';

function LGCarousel({items}){
    //use items to generate an array of html elements
    //const [itemElements, setItemElements] = useState();
    
    //Lightgallery needs to know it's container to display as in-line
    //const [container, setContainer] = useState(null);

    const onInit =useCallback((detail)=>{
        if (detail) {
            LightGallery.current = detail.instance;
            LightGallery.current.openGallery();
        }
    }, []);
    

    if(container !== null){
        return (
        <LightGallery 
            height={'100%'}
            slideDelay={400}
            closable= {false}
            plugins={[lgvideo]}
            //video settings:
            autoplayVideoOnSlide={true}
            preload={'none'}
            gotoNextSlideOnVideoEnd={true}

            onInit={onInit}
            dynamic={true} //allows galley to take array of items
            //Assuming items has an "src" property
            dynamicEl={items}
            >
        </LightGallery>
    )}
}