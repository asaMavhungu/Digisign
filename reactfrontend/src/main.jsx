import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import SigninPage from './pages/SigninPage.jsx'
import SlidesPage from './pages/SlidesPage.jsx'

import {
  createBrowserRouter,
  RouterProvider,
  Route,
} from 'react-router-dom'

const router = createBrowserRouter([
  {
    path: "/",
    element: <App/>,
  },

  {
    path: "SigninPage",
    element: <SigninPage/>,
  },

  {
    path: "SlidesPage",
    element: <SlidesPage/>,
  },
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router}/>
  </React.StrictMode>,
)
