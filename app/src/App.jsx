import { useState } from 'react'
import NavigationBar from './Components/NavigationBar'
import AboutUs from './Components/AboutUs.png.jsx'
import JobDetailsScreen from './Components/JobDetails.png.jsx'
import './App.css'
import Dashboard from './Components/Dashboard.png.jsx'

function App() {
  const [currentPage, setCurrentPage] = useState('home')
  const [selectedJob, setSelectedJob] = useState(null)

  const navigateToJobDetails = (jobTitle) => {
    setSelectedJob(jobTitle)
    setCurrentPage('jobdetails')
  }

  const renderPage = () => {
    switch (currentPage) {
      case 'about':
        return <AboutUs />
      case 'jobdetails':
        return <JobDetailsScreen jobTitle={selectedJob} />
      default:
        return <Dashboard onJobClick={navigateToJobDetails} />
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <NavigationBar currentPage={currentPage} setCurrentPage={setCurrentPage} />
      <main>
        {renderPage()}
      </main>
    </div>
  )
}

export default App
