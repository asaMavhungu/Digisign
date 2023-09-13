import './App.css'
import { Cards } from './components/Cards'


function App() {
  return <div className='App'>
    
    {/* Slides Card */}
    <Cards 
      imgSrc="https://assets.adidas.com/images/w_940,f_auto,q_auto/038bc994b2f24eaeb8dea991001bb3b9_9366/F35542_09_standard.jpg"
      imgAlt="Card Image"
      title="Slides"
      //description=
      buttonText="Click Here"
      link="SlidesPage"
    />

    {/* Signin Card */}
    <Cards 
      imgSrc="https://upload.wikimedia.org/wikipedia/commons/6/6a/Please_log_in_image.png"
      imgAlt="Card Image"
      title="Login"
      //description=
      buttonText="Click Here"
      link="SigninPage"
    />

  </div>

}

export default App
