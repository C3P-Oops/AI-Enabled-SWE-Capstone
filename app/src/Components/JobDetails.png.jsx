import React, { useState, useEffect } from 'react';
import AddApplicantModal from './AddApplicantModal.png.jsx';

// API base URL - adjust this to match your FastAPI server
const API_BASE_URL = 'http://localhost:8081';

const DocumentIcon = ({ className }) => (
  <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
  </svg>
);

const ChatIcon = ({ className }) => (
  <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
  </svg>
);

const UserIcon = ({ className }) => (
  <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
  </svg>
);

const PlaceholderIcon = ({ className }) => (
  <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

const ChevronDownIcon = ({ className }) => (
  <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
  </svg>
);

const LoadingSpinner = () => (
  <div className="flex justify-center items-center p-8">
    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
  </div>
);

// Helper function to format date
const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  });
};

// Helper function to transform API data to component format
const transformApplicationData = (applications, candidates) => {
  const candidateMap = candidates.reduce((acc, candidate) => {
    acc[candidate.candidate_id] = candidate;
    return acc;
  }, {});

  return applications.map((app) => {
    const candidate = candidateMap[app.candidate_id];
    return {
      id: app.application_id,
      name: candidate ? `${candidate.first_name} ${candidate.last_name}` : 'Unknown',
      date: formatDate(app.applied_at),
      status: app.status.charAt(0).toUpperCase() + app.status.slice(1).replace('_', ' '),
      resumeText: 'View',
      notesText: 'Add Notes',
      candidate_id: app.candidate_id,
      job_id: app.job_id
    };
  });
};

const StatusPill = ({ status }) => {
  const baseClasses = 'px-3 py-1 text-xs font-medium rounded-full inline-block';
  let specificClasses = '';

  switch (status.toLowerCase()) {
    case 'screening':
      specificClasses = 'bg-green-100 text-green-800';
      break;
    case 'interviewing':
      specificClasses = 'bg-orange-100 text-orange-800';
      break;
    case 'applied':
      specificClasses = 'bg-blue-100 text-blue-800';
      break;
    case 'rejected':
      specificClasses = 'bg-purple-100 text-purple-800';
      break;
    case 'offer extended':
      specificClasses = 'bg-red-100 text-red-800';
      break;
    case 'hired':
      specificClasses = 'bg-green-200 text-green-900';
      break;
    case 'withdrawn':
      specificClasses = 'bg-gray-100 text-gray-800';
      break;
    default:
      specificClasses = 'bg-gray-100 text-gray-800';
  }

  return <span className={`${baseClasses} ${specificClasses}`}>{status}</span>;
};


export default function JobDetailsScreen({ jobId = 1, jobTitle = "UI/UX Senior Product Designer", onBackToDashboard }) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedApplicantId, setSelectedApplicantId] = useState(1);
  const [jobData, setJobData] = useState(null);
  const [applicantsData, setApplicantsData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch job details and applications from API
  useEffect(() => {
    console.log('JobDetails: useEffect triggered with jobId:', jobId);
    
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        // If no jobId provided, show error
        if (!jobId) {
          throw new Error('No job ID provided');
        }

        console.log('JobDetails: Fetching data for job ID:', jobId);

        // Fetch job details
        const jobResponse = await fetch(`${API_BASE_URL}/jobs/${jobId}`);
        if (!jobResponse.ok) {
          throw new Error(`Failed to fetch job details: ${jobResponse.status}`);
        }
        const job = await jobResponse.json();

        // Fetch all applications
        const applicationsResponse = await fetch(`${API_BASE_URL}/applications/`);
        if (!applicationsResponse.ok) {
          throw new Error(`Failed to fetch applications: ${applicationsResponse.status}`);
        }
        const allApplications = await applicationsResponse.json();

        // Filter applications for this job
        const jobApplications = allApplications.filter(app => app.job_id === jobId);

        // Fetch all candidates to get names
        const candidatesResponse = await fetch(`${API_BASE_URL}/candidates/`);
        if (!candidatesResponse.ok) {
          throw new Error(`Failed to fetch candidates: ${candidatesResponse.status}`);
        }
        const candidates = await candidatesResponse.json();

        // Transform and set data
        setJobData(job);
        const transformedData = transformApplicationData(jobApplications, candidates);
        setApplicantsData(transformedData);
        
        // Set first applicant as selected if any exist
        if (transformedData.length > 0) {
          setSelectedApplicantId(transformedData[0].id);
        }

      } catch (err) {
        console.error('Error fetching data:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [jobId]);

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => {
    setIsModalOpen(false);
    // Refresh data when modal closes (in case new applicant was added)
    const refreshData = async () => {
      try {
        const applicationsResponse = await fetch(`${API_BASE_URL}/applications/`);
        const allApplications = await applicationsResponse.json();
        const jobApplications = allApplications.filter(app => app.job_id === jobId);
        
        const candidatesResponse = await fetch(`${API_BASE_URL}/candidates/`);
        const candidates = await candidatesResponse.json();
        
        const transformedData = transformApplicationData(jobApplications, candidates);
        setApplicantsData(transformedData);
      } catch (err) {
        console.error('Error refreshing data:', err);
      }
    };
    refreshData();
  };
  
  const handleRowClick = (applicantId) => {
    setSelectedApplicantId(applicantId);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 font-sans text-gray-800">
        <main className="container mx-auto p-8">
          <LoadingSpinner />
        </main>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 font-sans text-gray-800">
        <main className="container mx-auto p-8">
          <div className="bg-red-50 border border-red-200 rounded-md p-4">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error loading job details</h3>
                <div className="mt-2 text-sm text-red-700">
                  <p>{error}</p>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    );
  }

  const displayJobTitle = jobData?.title || jobTitle;

  return (
    <div className="min-h-screen bg-gray-50 font-sans text-gray-800">
      <main className="container mx-auto p-8">
        <div className="mb-6">
            <h2 className="text-lg font-semibold text-gray-600">Job Details</h2>
        </div>
        <div className="grid grid-cols-12 gap-8">
          {/* Left Column: Job Details */}
          <div className="col-span-12 lg:col-span-4">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">{displayJobTitle}</h3>
              
              <div className="space-y-6">
                <div>
                  <h4 className="font-semibold text-gray-700 mb-2">Description</h4>
                  <div className="text-gray-600 text-sm whitespace-pre-wrap">
                    {jobData?.description || 'No description available.'}
                  </div>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-700 mb-2">Job Information</h4>
                  <ul className="list-disc list-inside text-gray-600 space-y-2 text-sm">
                    <li>Job ID: {jobData?.job_id}</li>
                    <li>Created: {jobData?.created_at ? formatDate(jobData.created_at) : 'Unknown'}</li>
                    <li>Created by User ID: {jobData?.created_by_user_id}</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column: Applicants Table */}
          <div className="col-span-12 lg:col-span-8">
            <div className="bg-white rounded-lg shadow-md">
              <div className="p-6 flex justify-between items-center border-b border-gray-200">
                <h3 className="text-xl font-bold text-gray-900">
                  Applicants for {displayJobTitle} ({applicantsData.length})
                </h3>
                <button 
                  onClick={openModal}
                  className="bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Add New Applicant
                </button>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-sm text-left">
                  <thead className="text-xs text-gray-500 uppercase bg-gray-50">
                    <tr>
                      <th scope="col" className="px-6 py-3 font-medium">Applicant Name</th>
                      <th scope="col" className="px-6 py-3 font-medium">Application Date</th>
                      <th scope="col" className="px-6 py-3 font-medium">Status</th>
                      <th scope="col" className="px-6 py-3 font-medium">Resume/CV</th>
                      <th scope="col" className="px-6 py-3 font-medium">Feedback/Notes</th>
                    </tr>
                  </thead>
                  <tbody>
                    {applicantsData.length === 0 ? (
                      <tr>
                        <td colSpan="5" className="px-6 py-12 text-center text-gray-500">
                          <div className="flex flex-col items-center">
                            <UserIcon className="w-12 h-12 text-gray-300 mb-4" />
                            <p className="text-lg font-medium">No applicants yet</p>
                            <p className="text-sm">Add the first applicant to get started!</p>
                          </div>
                        </td>
                      </tr>
                    ) : (
                      applicantsData.map((applicant) => {
                        const isSelected = applicant.id === selectedApplicantId;
                        return (
                          <tr 
                            key={applicant.id} 
                            onClick={() => handleRowClick(applicant.id)}
                            className={`
                              border-b border-gray-200 cursor-pointer transition-all duration-200 ease-in-out
                              ${isSelected 
                                ? 'bg-blue-50 shadow-sm' 
                                : 'bg-white hover:bg-gray-50 hover:shadow-sm'
                              }
                              hover:scale-[1.01] hover:-translate-y-0.5
                            `}
                          >
                            <td className={`
                              px-6 py-4 font-medium whitespace-nowrap transition-colors duration-200
                              ${isSelected 
                                ? 'text-blue-600 border-l-4 border-blue-600' 
                                : 'text-gray-900'
                              }
                            `}>
                              {applicant.name}
                            </td>
                            <td className="px-6 py-4 text-gray-600">{applicant.date}</td>
                            <td className="px-6 py-4"><StatusPill status={applicant.status} /></td>
                            <td className="px-6 py-4">
                                <a href="#" className="flex items-center gap-2 text-gray-600 hover:text-gray-900 font-medium">
                                    {applicant.resumeText === 'Hired' && <UserIcon className="w-4 h-4" />}
                                    {applicant.resumeText === 'Haa' && <PlaceholderIcon className="w-4 h-4" />}
                                    {applicant.resumeText !== 'Hired' && applicant.resumeText !== 'Haa' && <DocumentIcon className="w-4 h-4" />}
                                    <span>{applicant.resumeText}</span>
                                </a>
                            </td>
                            <td className="px-6 py-4">
                              <div className="flex items-center justify-between">
                                <a href="#" className="flex items-center gap-2 text-gray-600 hover:text-gray-900 font-medium">
                                  <ChatIcon className="w-4 h-4" />
                                  <span>{applicant.notesText}</span>
                                </a>
                              </div>
                            </td>
                          </tr>
                        );
                      })
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 backdrop-blur-sm bg-white/30 flex items-center justify-center z-50">
          <div className="relative">
            <AddApplicantModal 
              jobTitle={displayJobTitle} 
              jobId={jobId}
              onClose={closeModal} 
            />
          </div>
        </div>
      )}
    </div>
  );
}