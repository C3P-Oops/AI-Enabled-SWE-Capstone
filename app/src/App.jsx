import { useState } from 'react'
import NavigationBar from './Components/NavigationBar'
import AboutUs from './Components/AboutUs.png.jsx'
import JobDetailsScreen from './Components/JobDetails.png.jsx'
import './App.css'
import Dashboard from './Components/Dashboard.png.jsx'

function App() {
  const [currentPage, setCurrentPage] = useState('home')
  const [selectedJob, setSelectedJob] = useState(null)
  const [selectedJobId, setSelectedJobId] = useState(null)

  const navigateToJobDetails = (jobId, jobTitle) => {
    // Handle both old signature (just title) and new signature (id, title)
    if (typeof jobId === 'string' && !jobTitle) {
      // Old signature: just job title was passed
      setSelectedJob(jobId)
      setSelectedJobId(null)
    } else {
      // New signature: jobId and jobTitle
      setSelectedJobId(jobId)
      setSelectedJob(jobTitle || `Job ${jobId}`)
    }
    setCurrentPage('jobdetails')
  }

  const navigateBackToDashboard = () => {
    setCurrentPage('home')
    setSelectedJob(null)
    setSelectedJobId(null)
  }

  const renderPage = () => {
    switch (currentPage) {
      case 'about':
        return <AboutUs />
      case 'jobdetails':
        return (
          <JobDetailsScreen 
            jobId={selectedJobId} 
            jobTitle={selectedJob}
            onBackToDashboard={navigateBackToDashboard}
          />
        )
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
