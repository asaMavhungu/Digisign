import React from 'react'
import CardItem from './CardItem'

function Cards() {
  return (
    <div className='cards'>
      <h1>Login</h1>
      <div className="cards__containter">
        <div className="cards__wrapper">
            <ul className="cards__items">
                <CardItem />
            </ul>
        </div>
      </div>
    </div>
  )
}

export default Cards
