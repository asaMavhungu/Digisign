import './App.css'
import { Cards } from './components/Cards'

function App() {
  return <div className='App'>
    <Cards 
      imgSrc="https://upload.wikimedia.org/wikipedia/commons/6/6a/Please_log_in_image.png"
      imgAlt="Card Image"
      title="Login"
      //description=
      buttonText="Click Here"
      link="cardPage"
    />
  </div>
}

export default App
