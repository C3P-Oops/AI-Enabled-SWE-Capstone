import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import Dashboard from './Components/Dashboard.png.jsx'
import JobDetailsScreen from './Components/JobDetails.png.jsx'
import AddApplicantModal from './Components/AddApplicantModal.png.jsx'
import AboutUsPage from './Components/AboutUs.png.jsx'
import NavigationBar from './Components/NavigationBar.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    {/* <NavigationBar />
    <Dashboard /> */}
    <App />
  </StrictMode>,
)
