import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'
import { BackendProvider } from './services/backendService'
import { BrowserRouter as Router } from 'react-router-dom'

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <Router>
  <React.StrictMode>
     <BackendProvider>
     <App />
    </BackendProvider>
  </React.StrictMode>
  </Router>,
)
