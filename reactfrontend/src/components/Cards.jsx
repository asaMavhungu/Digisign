import React from 'react'
import "./Cards.css"

export const Cards = ({
    imgSrc,
    imgAlt,
    title,
    //description,
    buttonText,
    link,
}) => {
  return (
    <div className='card-container'>
        {imgSrc && imgAlt && <img src={imgSrc} 
        alt={imgAlt} className='card-img'
        style={{width: "300px", height: "auto"}}
        />}
        {title && <h1 className='card-title'>{title}</h1>}
        {buttonText && link && <a href= {link} className='card-btn'>{buttonText}</a>}
    </div>
  )
}